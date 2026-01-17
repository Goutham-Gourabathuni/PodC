import os
from faster_whisper import WhisperModel
import logging

logger = logging.getLogger(__name__)

# Configuration
MODEL_SIZE = os.getenv("WHISPER_MODEL_SIZE", "tiny")
DEVICE = "cpu" # Force CPU for compatibility, user can change to "cuda" if needed
COMPUTE_TYPE = "int8"

_model = None

def get_model():
    global _model
    if _model is None:
        logger.info(f"Loading Whisper model: {MODEL_SIZE} on {DEVICE}")
        _model = WhisperModel(MODEL_SIZE, device=DEVICE, compute_type=COMPUTE_TYPE)
    return _model

def transcribe_audio(file_path: str) -> dict:
    """
    Transcribes audio file using Faster Whisper.
    Returns dictionary with text and segments.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    model = get_model()
    
    logger.info(f"Starting transcription for {file_path}")
    segments, info = model.transcribe(file_path, beam_size=5)
    
    # helper to consume the generator
    full_text = []
    segment_data = []
    
    for segment in segments:
        full_text.append(segment.text)
        segment_data.append({
            "start": segment.start,
            "end": segment.end,
            "text": segment.text
        })
        
    return {
        "text": " ".join(full_text).strip(),
        "language": info.language,
        "duration": info.duration,
        "segments": segment_data
    }
