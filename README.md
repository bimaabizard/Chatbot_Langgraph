# Enterprise Stateful AI Agent API

A production-ready microservice demonstrating stateful, multi-turn LLM interactions using LangGraph, with distributed memory management backed by Redis.

## 🧠 Architecture Overview
*   **Routing & Orchestration:** LangGraph (StateGraph)
*   **State Persistence:** Redis (via `langgraph-checkpoint-redis`) for thread-level memory across distributed API instances.
*   **API Layer:** FastAPI
*   **Observability:** Prometheus integration for tracking `/chat` endpoint latency and request volume.
*   **Infrastructure:** Fully containerized via Docker, utilizing `uv` for optimized dependency installation.

## 💡 The Engineering Challenge Solved
Standard LLM wrappers lose conversation context or rely on local, in-memory arrays (which fail the moment the app scales to multiple workers). By injecting a **Redis checkpointer** into the LangGraph configuration, this API ensures that user `thread_id` states are instantly hydrated from the cache, enabling true stateless horizontal scaling of the API servers while preserving long-term conversational memory.

## 🚀 Quick Start
```bash
# Add API KEYS
export OPENAI_API_KEY="sk-..."

# Build and boot the stack (API, Redis cache, Prometheus)
docker-compose up --build