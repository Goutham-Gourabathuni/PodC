from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

from backend.database import init_db

app = FastAPI(
    title="Podcast Summarization API",
    description="Backend for podcast summarization service",
    version="0.1.0"
)

# Initialize database tables
init_db()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "Podcast Summarization API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}

from backend.auth import router as auth_router
from backend.pipeline import router as pipeline_router

app.include_router(auth_router)
app.include_router(pipeline_router)

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=5000, reload=True)
