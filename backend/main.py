from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
import uuid

from backend.database import init_db
from fastapi.staticfiles import StaticFiles
# auth and pipeline routes
from backend.auth import router as auth_router
from backend.pipeline import router as pipeline_router

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

# health check endpoints
@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "Podcast Summarization API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}

# auth and pipeline routes
from backend.auth import router as auth_router
from backend.pipeline import router as pipeline_router

app.include_router(auth_router)
app.include_router(pipeline_router)

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=5000, reload=True)

# audio storage code and endpoints
AUDIO_STORAGE = "backend/storage/audio"
os.makedirs(AUDIO_STORAGE, exist_ok=True)

@app.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...)):
    """
    Upload any podcast audio file and store it locally.
    """
    file_id = str(uuid.uuid4())
    file_extension = os.path.splitext(file.filename)[1]
    filename = f"{file_id}{file_extension}"

    file_path = os.path.join(AUDIO_STORAGE, filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    return JSONResponse({
        "podcast_id": file_id,
        "file_path": file_path
    })

app.mount("/backend/storage", StaticFiles(directory="backend/storage"), name="storage")

app.mount(
    "/generated_reports",
    StaticFiles(directory="generated_reports"),
    name="generated_reports"
)
