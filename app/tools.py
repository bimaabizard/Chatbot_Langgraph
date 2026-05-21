import os
import json
from typing import Optional
from langchain_core.tools import tool
# from langchain_openai import OpenAIEmbeddings
# from langchain_community.vectorstores import PGVector  # Or Chroma, FAISS, Pinecone

@tool
def retrieve_knowledge_base_documents(query: str, category: Optional[str] = None) -> str:
    """
    Search and retrieve relevant technical documentation, legal codes, and internal standard 
    operating procedures (SOPs) from the vector database.
    Use this tool when the user asks for historical guidelines, policy explanations, or documentation.
    
    Args:
        query: The semantic search query or keywords.
        category: Optional filter to restrict search to a specific domain (e.g., 'legal', 'technical', 'finance').
    """
    # In a production environment, you would instantiate your embeddings and connect to your VectorDB:
    # embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    # vector_store = PGVector(connection_string=os.getenv("DATABASE_URL"), embedding_function=embeddings)
    
    try:
        # Simulating metadata-filtered vector search results
        logger_msg = f"Executing vector similarity search for: '{query}'"
        if category:
            logger_msg += f" with metadata filter: [category == '{category}']"
            
        # Mocking the semantic search match payloads
        mock_chunks = [
            {
                "document_id": "DOC-2026-892",
                "title": "Standard Operating Procedures for AI Microservices",
                "content": "All stateful AI workflows deployed to production environments must utilize external persistence layers like Redis for checkpointing to guarantee horizontal scalability across distributed nodes.",
                "score": 0.89,
                "metadata": {"category": "technical", "author": "Architecture Team"}
            },
            {
                "document_id": "DOC-2025-114",
                "title": "Corporate Compliance and Data Governance Policy",
                "content": "User context, persistent identifiers, and session data must be isolated per tenant. Data transiently processed by large language models must satisfy regional privacy standards.",
                "score": 0.74,
                "metadata": {"category": "legal", "author": "Compliance Legal"}
            }
        ]
        
        # Apply the metadata filter if provided
        if category:
            filtered_chunks = [c for c in mock_chunks if c["metadata"]["category"] == category.lower()]
        else:
            filtered_chunks = mock_chunks

        # If no documents match the filter
        if not filtered_chunks:
            return json.dumps({"status": "success", "results": [], "message": f"No documents found matching category: {category}"})

        return json.dumps({
            "status": "success",
            "search_query": query,
            "filter_applied": category if category else "none",
            "results": filtered_chunks
        })
        
    except Exception as e:
        return f"Vector retrieval failed: {str(e)}"

@tool
def query_corporate_database(sql_query: str) -> str:
    """
    Query the internal PostgreSQL database to retrieve live transactional metrics and user data.
    Use this tool ONLY when the user explicitly asks for live internal company metrics.
    """
    try:
        mock_data = {
            "status": "success",
            "executed_query": sql_query,
            "results": [
                {"metric": "daily_active_users", "value": 1420},
                {"metric": "system_uptime", "value": "99.98%"}
            ]
        }
        return json.dumps(mock_data)
    except Exception as e:
        return f"Database execution failed: {str(e)}"

@tool
def search_external_intelligence(query: str) -> str:
    """
    Search external sources using SearXNG to retrieve up-to-date internet information.
    Use this tool to find news, current events, or documentation not in the LLM's weights.
    """
    try:
        return f"SearXNG results for '{query}': Recent infrastructure updates indicate heavy corporate shift toward containerized RAG systems."
    except Exception as e:
        return f"Search service unavailable: {str(e)}"

# Update the exported tools array so agent.py automatically binds all three capabilities
agent_tools = [retrieve_knowledge_base_documents, query_corporate_database, search_external_intelligence]