import logging
from langchain_community.chat_models import BedrockChat
from langchain_community.embeddings import BedrockEmbeddings
from langchain_community.vectorstores import OpenSearchVectorSearch
from langchain_core.documents import Document

from langchain_core.prompts import ChatPromptTemplate

from langchain_open_search import OpenSearchSettings  # custom config
import boto3
import os

# === CONFIG VARIABLES ===
OPENSEARCH_HOST = os.environ.get("jumud3coizfqh7wcw2eh.us-east-1.aoss.amazonaws.com")
OPENSEARCH_PORT = 443
EMBEDDING_MODEL_ID = "amazon.titan-embed-text-v1"



# === Initialize Bedrock Embeddings ===
def get_bedrock_embedding_client():
    try:
        embedding_client = BedrockEmbeddings(
            model_id=EMBEDDING_MODEL_ID,
            region_name="us-east-1"
        )
        logging.info(f"Initialized BedrockEmbeddings client for model {EMBEDDING_MODEL_ID}")
        return embedding_client
    except Exception as e:
        logging.error(f"Error initializing BedrockEmbeddings: {e}")
        raise

# === Initialize OpenSearch Vector Search ===
def get_search_client(index_name):
    try:
        opensearch_client = OpenSearchVectorSearch(
            index_name=index_name,
            embedding=get_bedrock_embedding_client(),
            opensearch_url=OPENSEARCH_HOST,
            port=OPENSEARCH_PORT,
            use_ssl=True,
            verify_certs=True,
            connection_class='requests'
        )
        logging.info(f"Initialized OpenSearchVectorSearch for index {index_name}")
        return opensearch_client
    except Exception as e:
        logging.error(f"Error initializing OpenSearchVectorSearch: {e}")
        raise

# === Get Embeddings (vectorize input text) ===
async def get_embeddings(text: str):
    try:
        embedding_client = get_bedrock_embedding_client()
        embeddings = await embedding_client.aembed_documents([text])
        return embeddings
    except Exception as e:
        logging.error(f"Error generating embeddings: {e}")
        raise

# === Search for Instructions ===
async def search_instructions(query_text: str, index_name: str, k=10):
    try:
        opensearch_client = get_search_client(index_name)
        results = opensearch_client.similarity_search(query_text, k=k)
        response_list = [r.page_content for r in results]
        return response_list
    except Exception as e:
        logging.error(f"Error performing semantic search in instructions index: {e}")
        return []

# === Search for Domain Documents ===
async def search_documents(query_text: str, index_name: str, k=10):
    try:
        opensearch_client = get_search_client(index_name)
        results = opensearch_client.similarity_search(query_text, k=k)
        domains = [r.page_content for r in results]
        return domains
    except Exception as e:
        logging.error(f"Error performing domain document search: {e}")
        return []
