FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    MEDIA_DIR=/tmp/podc-media \
    HF_HOME=/data/.cache/huggingface \
    TRANSFORMERS_CACHE=/data/.cache/huggingface \
    WHISPER_MODEL=base \
    SUMMARIZER_MODEL=facebook/bart-large-cnn \
    EMBEDDING_MODEL=all-MiniLM-L6-v2 \
    SPACY_MODEL=en_core_web_sm \
    GEMINI_MODEL=gemini-2.5-flash

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg git build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements-backend.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements-backend.txt \
    && python -m nltk.downloader punkt punkt_tab

COPY backend backend
COPY pipeline pipeline

RUN mkdir -p "$MEDIA_DIR/uploads" "$MEDIA_DIR/chunks" "$MEDIA_DIR/pdfs" "$HF_HOME"

EXPOSE 8080

CMD ["uvicorn","backend.main:app","--host","0.0.0.0","--port","8080"]
