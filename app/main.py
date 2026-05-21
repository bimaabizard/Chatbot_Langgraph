from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from prometheus_fastapi_instrumentator import Instrumentator
from app.agent import get_compiled_graph

app = FastAPI(title="Enterprise Agent API")

# 1. Setup Jinja2 to point to your new template folder
templates = Jinja2Templates(directory="template")

Instrumentator().instrument(app).expose(app)
agent_graph = get_compiled_graph()

class ChatRequest(BaseModel):
    thread_id: str
    message: str

# 2. Serve the Vue.js frontend on the root route
@app.get("/")
async def serve_frontend(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    # ... (Keep your existing chat_endpoint logic here)
    try:
        config = {"configurable": {"thread_id": req.thread_id}}
        inputs = {"messages": [("user", req.message)]}
        
        result = agent_graph.invoke(inputs, config=config)
        
        return {
            "thread_id": req.thread_id,
            "response": result["messages"][-1].content
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))