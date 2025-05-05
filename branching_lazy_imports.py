import time
start_time = time.time()
import os
import boto3
from langchain_core.messages import ToolMessage, AIMessage
from langchain_core.runnables import RunnableWithFallbacks
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langgraph.graph import END, StateGraph, START
from langgraph.graph.message import AnyMessage, add_messages
from typing import Any, Annotated, Literal, List, Dict, AsyncGenerator
from typing_extensions import TypedDict
import prompts
from langchain_community.utilities import SQLDatabase
from langchain_aws import BedrockChat
import json


# Setup AWS Bedrock client via boto3
boto3_bedrock_client = boto3.client(service_name="bedrock-runtime", region_name="us-east-1")

def get_db_credentials(secret_name, region_name):
    # Create a Secrets Manager client
    client = boto3.client('secretsmanager', region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        secret = get_secret_value_response['SecretString']
        return json.loads(secret)
    except Exception as e:
        raise RuntimeError(f"Error fetching secret: {e}")

# Usage
secret_name = "rds!db-61356bef-a57d-4113-804b-1a56b3722416"
region_name = "us-east-1"
creds = get_db_credentials(secret_name, region_name)

# --- PostgreSQL connection (AWS RDS) ---
db_params = {
    'host': "database-power-assist.cevefiaq0e14.us-east-1.rds.amazonaws.com",
    'database': "sampleDB",
    'user': creds['username'],
    'password': creds['password'],
    'port': "5432"
}

db = SQLDatabase.from_uri(
    f"postgresql://{db_params['user']}:{db_params['password']}@{db_params['host']}:5432/{db_params['database']}"
)

# --- Prompts & LLM setup ---
answer_gen_prompt = ChatPromptTemplate.from_messages([
    ("system", prompts.answer_gen_system),
    ("placeholder", "{messages}")
])

answer_gen = answer_gen_prompt | BedrockChat(
    model_id="meta.llama3-70b-instruct-v1:0",
    client=boto3_bedrock_client,
    temperature=0
)

query_gen_prompt = ChatPromptTemplate.from_messages([
    ("system", prompts.query_gen_system),
    ("placeholder", "{messages}")
])

query_gen = query_gen_prompt | BedrockChat(
    model_id="meta.llama3-70b-instruct-v1:0",
    client=boto3_bedrock_client,
    temperature=0
)

llm = BedrockChat(
    model_id="meta.llama3-70b-instruct-v1:0",
    client=boto3_bedrock_client,
    temperature=0
)

class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

toolkit = SQLDatabaseToolkit(db=db, llm=llm)
tools = toolkit.get_tools()
list_tables_tool = next(tool for tool in tools if tool.name == "sql_db_list_tables")
get_schema_tool = next(tool for tool in tools if tool.name == "sql_db_schema")

def create_tool_node_with_fallback(tools: list) -> RunnableWithFallbacks[Any, dict]:
    from langchain_core.runnables import RunnableLambda
    from langgraph.prebuilt import ToolNode
    return ToolNode(tools).with_fallbacks(
        [RunnableLambda(handle_tool_error)], exception_key="error"
    )

def handle_tool_error(state) -> dict[str, list[ToolMessage]]:
    error = state.get("error")
    tool_calls = state["messages"][-1].tool_calls
    return {
        "messages": [
            ToolMessage(
                content=f"Error: {repr(error)}\n please fix your mistakes.",
                tool_call_id=tc["id"],
            )
            for tc in tool_calls
        ]
    }

def first_tool_call(state: State) -> dict[str, list[AIMessage]]:
    return {
        "messages": [
            AIMessage(
                content="",
                tool_calls=[{
                    "name": "sql_db_list_tables",
                    "args": {},
                    "id": "tool_abcd123",
                }],
            )
        ]
    }

@tool
def get_table_schema_tool(table_name='new_data') -> str:
    from table_schema import table_schema
    schema = get_schema_tool.invoke(table_name)
    schema = table_schema + schema
    return schema

model_get_schema = BedrockChat(
    model_id="meta.llama3-70b-instruct-v1:0",
    client=boto3_bedrock_client,
    temperature=0
).bind_tools([get_table_schema_tool])

@tool
def db_query_tool(query: str) -> str:
    result = db.run_no_throw(query)
    if not result:
        return "Error: Query failed. Please rewrite your query and try again."
    return result

@tool
def get_instructions_tool(query: str) -> str:
    from similarity_search import get_instructions_domains
    if not query:
        return "Error: No user query provided."
    instructions_domains = get_instructions_domains(query)
    return instructions_domains

model_get_instructions = BedrockChat(
    model_id="meta.llama3-70b-instruct-v1:0",
    client=boto3_bedrock_client,
    temperature=0
).bind_tools([get_instructions_tool])

query_check_prompt = ChatPromptTemplate.from_messages([
    ("system", prompts.query_check_system),
    ("placeholder", "{messages}")
])
query_check = query_check_prompt | BedrockChat(
    model_id="meta.llama3-70b-instruct-v1:0",
    client=boto3_bedrock_client,
    temperature=0
).bind_tools([db_query_tool], tool_choice="required")

def model_check_query(state: State) -> dict[str, list]:
    messages = [message for message in state["messages"]]
    message = query_gen.invoke({"messages": messages})
    return {"messages": [message]}

def answer_gen_node(state: State) -> dict[str, list]:
    messages = [message for message in state["messages"]]
    message = answer_gen.invoke({"messages": messages})
    return {"messages": [message]}

def query_gen_node(state: State):
    messages = [message for message in state["messages"]]
    message = query_gen.invoke({"messages": messages})
    return {"messages": [message]}

def execute_query_node(state: State):
    messages = [message for message in state["messages"]]
    query = messages[-1].content.replace("```sql", "").replace("```", "")
    message = db_query_tool.invoke(query)
    return {"messages": [message]}

@tool
def get_related_metrics(query: str) -> str:
    relations = prompts.relations
    return relations

model_get_related_metrics = BedrockChat(
    model_id="meta.llama3-70b-instruct-v1:0",
    client=boto3_bedrock_client,
    temperature=0
).bind_tools([get_related_metrics])

graph_gen_prompt = ChatPromptTemplate.from_messages([
    ("system", prompts.graph_prompt),
    ("placeholder", "{messages}")
])
model_graph_gen = graph_gen_prompt | BedrockChat(
    model_id="meta.llama3-70b-instruct-v1:0",
    client=boto3_bedrock_client,
    temperature=0
)

def graph_gen_node(state: State) -> dict[str, list]:
    messages = [message for message in state["messages"]]
    message = model_graph_gen.invoke({"messages": messages})
    return {"messages": [message]}

bi_gen_prompt = ChatPromptTemplate.from_messages([
    ("system", prompts.bi_ans_prompt),
    ("placeholder", "{messages}")
])
bi_answer_gen = bi_gen_prompt | BedrockChat(
    model_id="meta.llama3-70b-instruct-v1:0",
    client=boto3_bedrock_client,
    temperature=0
)

def bi_gen_node(state: State):
    messages = [message for message in state["messages"]]
    message = bi_answer_gen.invoke({"messages": messages})
    return {"messages": [message]}

def sink_node(state: State):
    messages_a = [message for message in state["messages"]]
    return {"messages": messages_a}

builder = StateGraph(State)
builder.add_node("first_tool_call", first_tool_call)
builder.add_node("list_tables_tool", create_tool_node_with_fallback([list_tables_tool]))
builder.add_node("model_get_schema", lambda state: {"messages": [model_get_schema.invoke([msg for msg in state["messages"]])]})
builder.add_node("get_instructions_tool", create_tool_node_with_fallback([get_instructions_tool]))
builder.add_node("get_table_schema_tool", create_tool_node_with_fallback([get_table_schema_tool]))
builder.add_node("model_get_instructions", lambda state: {"messages": [model_get_instructions.invoke([msg for msg in state["messages"]])]})
builder.add_node("query_gen", query_gen_node)
builder.add_node("ans_gen", answer_gen_node)
builder.add_node("correct_query", model_check_query)
builder.add_node("execute_query", execute_query_node)
builder.add_node("model_get_related_metrics", lambda state: {"messages": [model_get_related_metrics.invoke([msg for msg in state["messages"]])]})
builder.add_node("get_related_metrics", create_tool_node_with_fallback([get_related_metrics]))
builder.add_node("get_related_metrics", create_tool_node_with_fallback([get_related_metrics]))
builder.add_node("bi_ans_gen", bi_gen_node)
builder.add_node("graph_gen", graph_gen_node)
builder.add_node("sink_node", sink_node)

builder.add_edge(START, "first_tool_call")
builder.add_edge("first_tool_call", "list_tables_tool")
builder.add_edge("list_tables_tool", "model_get_schema")
builder.add_edge("model_get_schema", "get_table_schema_tool")
builder.add_edge("get_table_schema_tool", "model_get_instructions")
builder.add_edge("model_get_instructions", "get_instructions_tool")
builder.add_edge("get_instructions_tool", "model_get_related_metrics")
builder.add_edge("model_get_related_metrics", "get_related_metrics")
builder.add_edge("get_related_metrics", "query_gen")
builder.add_edge("query_gen", "execute_query")
builder.add_edge("execute_query", "ans_gen")
builder.add_edge("execute_query", "bi_ans_gen")
builder.add_edge("execute_query", "graph_gen")
builder.add_edge("bi_ans_gen", "sink_node")
builder.add_edge("graph_gen", "sink_node")
builder.add_edge("ans_gen", "sink_node")
builder.add_edge("sink_node", END)

graph = builder.compile()

response = graph.invoke({
    "messages": [("user", "What are the leading brands within the Global region based on net sales?")]
})

time_taken = time.time() - start_time

for msg in response["messages"]:
    print(msg.content)

print(f"Total time taken to get the response: {time_taken}s")
