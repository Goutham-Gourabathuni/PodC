from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, UploadFile, File, Form
from sqlalchemy.orm import Session
from backend.database import get_db, SessionLocal
from backend.models import Podcast, Result, SourceType, User
from backend.services import audio, transcription, nlp, report
import logging
import os
import asyncio

router = APIRouter(prefix="/pipeline", tags=["Pipeline"])
logger = logging.getLogger(__name__)

async def process_podcast_background(podcast_id: int):
    """
    Background task to process the podcast: download -> transcribe -> summarize -> report.
    """
    db = SessionLocal()
    try:
        podcast = db.query(Podcast).filter(Podcast.id == podcast_id).first()
        if not podcast:
            logger.error(f"Podcast {podcast_id} not found.")
            return

        real_audio_path = podcast.audio_path
        
        # 1. Download if URL
        if podcast.source_type == SourceType.URL:
            try:
                # Assuming audio_path holds the URL
                logger.info(f"Downloading audio from {podcast.audio_path}")
                real_audio_path = await audio.download_audio_from_url(podcast.audio_path)
            except Exception as e:
                logger.error(f"Download failed for {podcast_id}: {e}")
                return

        # 2. Transcribe (Sync function, run in threadpool if needed, but it releases GIL usually)
        # Since it's CPU bound, running it directly in async loop might block. 
        # For simplicity in this demo, we'll run it directly or wrap in to_thread.
        logger.info(f"Transcribing {real_audio_path}")
        transcription_result = await asyncio.to_thread(transcription.transcribe_audio, real_audio_path)
        transcript_text = transcription_result["text"]
        
        # 3. NLP
        logger.info("Generating summary")
        summary = nlp.generate_summary(transcript_text)
        topics = nlp.extract_topics(transcript_text)
        
        # 4. Report
        pdf_filename = f"summary_{podcast_id}.pdf"
        output_dir = "generated_reports"
        os.makedirs(output_dir, exist_ok=True)
        pdf_path = os.path.join(output_dir, pdf_filename)
        
        report.generate_pdf_report(podcast.title, summary, topics, pdf_path)
        
        # 5. Save Result
        result = Result(
            podcast_id=podcast.id,
            transcript=transcript_text,
            summary=summary,
            topics=topics,  # Database model expects JSON
            pdf_path=pdf_path
        )
        db.add(result)
        db.commit()
        logger.info(f"Processing complete for {podcast_id}")
        
    except Exception as e:
        logger.error(f"Error processing podcast {podcast_id}: {e}")
    finally:
        db.close()

@router.post("/upload")
async def upload_podcast(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    title: str = Form(...),
    db: Session = Depends(get_db)
):
    # TODO: Get current user. Using dummy user ID 1 for now.
    user_id = 1 
    
    # Save file
    saved_path = await audio.save_upload_file(file)
    
    # Create DB Entry
    podcast = Podcast(
        user_id=user_id,
        title=title,
        source_type=SourceType.UPLOAD,
        audio_path=saved_path
    )
    db.add(podcast)
    db.commit()
    db.refresh(podcast)
    
    # Trigger background task
    background_tasks.add_task(process_podcast_background, podcast.id)
    
    return {"message": "Podcast uploaded and processing started", "podcast_id": podcast.id}

@router.post("/submit_url")
async def submit_podcast_url(
    background_tasks: BackgroundTasks,
    url: str,
    title: str,
    db: Session = Depends(get_db)
):
    # TODO: Get current user
    user_id = 1
    
    podcast = Podcast(
        user_id=user_id,
        title=title,
        source_type=SourceType.URL,
        audio_path=url # Store URL initially
    )
    db.add(podcast)
    db.commit()
    db.refresh(podcast)
    
    background_tasks.add_task(process_podcast_background, podcast.id)
    
    return {"message": "Podcast URL submitted and processing started", "podcast_id": podcast.id}

@router.get("/status/{podcast_id}")
def get_podcast_status(podcast_id: int, db: Session = Depends(get_db)):
    podcast = db.query(Podcast).filter(Podcast.id == podcast_id).first()
    if not podcast:
        raise HTTPException(status_code=404, detail="Podcast not found")

    result = db.query(Result).filter(Result.podcast_id == podcast_id).first()

    if not result:
        return {"status": "processing"}

    return {
        "status": "completed",
        "summary": result.summary,
        "topics": result.topics,
        "pdf_path": result.pdf_path
    }
