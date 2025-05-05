from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from branching_lazy_imports import graph
from langchain_core.messages import HumanMessage
import uvicorn
from langchain.prompts import PromptTemplate
from models import SearchRequest, SearchResponse, SearchResultItem
from embedding import get_embedding_from_bedrock,search_similar_documents

app = FastAPI(
    title="AWS RAG Chatbot",
    description="Chatbot powered by AWS Bedrock, OpenSearch, RDS, FastAPI",
    version="1.0"
)

@app.get("/")
async def root():
    return {"message": "AWS RAG Chatbot is running!"}

@app.post("/ask", response_model=SearchResponse)
def ask_api(request: SearchRequest):
    import time
    start_time = time.time()

    try:
        # Create input messages
        input_messages = [HumanMessage(content=request.query)]

        # Invoke the LangGraph
        response = graph.invoke({"messages": input_messages})

        responses = [msg.content for msg in response["messages"]]
        time_taken = time.time() - start_time

        return SearchResponse(responses=responses, time_taken=time_taken)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search/", response_model=SearchResponse)
async def search_docs(search_req: SearchRequest):
    try:
        embedding = get_embedding_from_bedrock(search_req.query)
        results = search_similar_documents(embedding, search_req.top_k)
        response_items = [
            SearchResultItem(
                source_file=doc["source_file"],
                text=doc["text"],
                score=doc["_score"]
            )
            for doc in results
        ]
        return SearchResponse(results=response_items)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search error: {e}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
