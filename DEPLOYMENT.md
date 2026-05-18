# PodC Deployment Notes

## Backend on HuggingFace Spaces

Use the root `Dockerfile` for a Docker Space. Add these environment variables in the Space settings:

```bash
GEMINI_API_KEY=your_gemini_api_key
CORS_ORIGINS=https://your-frontend-domain.example
```

Optional model overrides:

```bash
WHISPER_MODEL=base
SUMMARIZER_MODEL=facebook/bart-large-cnn
EMBEDDING_MODEL=all-MiniLM-L6-v2
SPACY_MODEL=en_core_web_sm
GEMINI_MODEL=gemini-2.5-flash
```

Optional runtime media directory:

```bash
MEDIA_DIR=/tmp/podc-media
```

The backend exposes:

- `GET /health` for uptime checks
- `GET /models` for the configured model stack
- `POST /process` for audio upload and analysis
- `GET /ask?question=...` for podcast Q&A
- `POST /download-pdf` for summary PDF export

## React Frontend

Deploy `frontend-react/dist` to a static host. Before building, set:

```bash
VITE_API_BASE_URL=https://your-huggingface-space.hf.space
```

Then build:

```bash

npm install
npm run build

if any issue, the first 'cd frontend-react' and then use the other 2 commands
```

The deployed site will call the Railway backend directly through the configured API URL.
