from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

import shutil
import os
import uuid
import tempfile
from threading import Lock
from pathlib import Path

from pipeline.workflow_main import run_pipeline
from pipeline.pdf_exporter import generate_pdf
from pipeline.gemini_qa import answer_question
# from pipeline.openai_qa import answer_question  # switch later if needed

# -----------------------------
# App setup
# -----------------------------

app = FastAPI(title="PodC Backend")


def _parse_cors_origins():
    raw_origins = os.getenv("CORS_ORIGINS", "")
    origins = [origin.strip() for origin in raw_origins.split(",") if origin.strip()]
    return origins


def _cors_origin_regex():
    return os.getenv(
        "CORS_ORIGIN_REGEX",
        r"https?://(localhost|127\.0\.0\.1|0\.0\.0\.0|192\.168\.\d+\.\d+|10\.\d+\.\d+\.\d+|172\.(1[6-9]|2\d|3[0-1])\.\d+\.\d+)(:\d+)?"
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=_parse_cors_origins(),
    allow_origin_regex=_cors_origin_regex(),
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

DEFAULT_MEDIA_DIR = Path(tempfile.gettempdir()) / "podc-media"
MEDIA_DIR = Path(os.getenv("MEDIA_DIR", DEFAULT_MEDIA_DIR))
UPLOAD_DIR = MEDIA_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

MODEL_CONFIG = {
    "asr": os.getenv("WHISPER_MODEL", "base"),
    "summarizer": os.getenv("SUMMARIZER_MODEL", "facebook/bart-large-cnn"),
    "embeddings": os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2"),
    "qa": os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
    "topic_titles": os.getenv("SPACY_MODEL", "en_core_web_sm"),
}

# -----------------------------
# Global in-memory state
# -----------------------------

LAST_TRANSCRIPT_TEXT = ""
run_pipeline_last_result = None
PROCESS_LOCK = Lock()

# -----------------------------
# Health check and root
# -----------------------------

@app.get("/")
def root():
    return {
        "status": "Backend is working",
        "message": "PodC API is ready."
    }

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/models")
def models():
    return {
        "status": "configured",
        "models": MODEL_CONFIG,
        "notes": {
            "asr": "OpenAI Whisper runs locally inside the backend runtime.",
            "summarizer": "HuggingFace Transformers pipeline loads lazily on first summary request.",
            "embeddings": "SentenceTransformers loads lazily on first podcast processing request.",
            "qa": "Gemini requires GEMINI_API_KEY to be set in the backend environment.",
        }
    }

# -----------------------------
# Process podcast
# -----------------------------

@app.post("/process")
async def process_podcast(file: UploadFile = File(...)):
    global LAST_TRANSCRIPT_TEXT, run_pipeline_last_result

    if not PROCESS_LOCK.acquire(blocking=False):
        raise HTTPException(
            status_code=409,
            detail="Another podcast is already being processed. Please wait for it to finish."
        )

    try:
        # 1️⃣ Save uploaded file
        ext = os.path.splitext(file.filename)[1]
        filename = f"{uuid.uuid4()}{ext}"
        file_path = UPLOAD_DIR / filename

        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 2️⃣ Run pipeline ONCE
        result = run_pipeline(str(file_path))

        # 3️⃣ Store global state for Q&A + PDF
        transcript = result.get("transcript", [])
        LAST_TRANSCRIPT_TEXT = " ".join(
            seg.get("text", "") for seg in transcript
        )
        run_pipeline_last_result = result

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        PROCESS_LOCK.release()

# -----------------------------
# Q&A endpoint (Gemini)
# -----------------------------

@app.get("/ask")
def ask_question(question: str):
    if not LAST_TRANSCRIPT_TEXT:
        return {"answer": "No podcast has been processed yet."}

    try:
        answer = answer_question(
            question=question,
            context=LAST_TRANSCRIPT_TEXT
        )
        return {"answer": answer}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -----------------------------
# Download PDF
# -----------------------------

@app.post("/download-pdf")
def download_pdf():
    try:
        if not run_pipeline_last_result:
            raise HTTPException(
                status_code=400,
                detail="No podcast processed yet"
            )

        pdf_path = generate_pdf(
            topics=run_pipeline_last_result["topics"],
            episode_summary=run_pipeline_last_result.get("episode_summary")
        )

        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename="podc_summary.pdf"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.on_event("startup")
async def startup():
    import os
    print("PORT =", os.getenv("PORT"))
    print("Current dir =", os.getcwd())
    
@app.get("/ping")
def ping():
    return {"pong": True}
