from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from api.auth import router as auth_router
from api.schemes import router as schemes_router
from api.complaints import router as complaints_router
from api.documents import router as documents_router
from pydantic import BaseModel

app = FastAPI(title="SmartBharat AI API", version="1.0.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For development, we'll allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api")
app.include_router(schemes_router, prefix="/api")
app.include_router(complaints_router, prefix="/api")
app.include_router(documents_router, prefix="/api")

class ChatRequest(BaseModel):
    message: str
    user_id: str

@app.get("/")
def read_root():
    return {"message": "Welcome to SmartBharat AI API"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    from agents.router import process_chat
    res = process_chat(req.message)
    return {
        "response": res["response"],
        "agent": res["agent"],
        "suggested_actions": res["suggested_actions"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
