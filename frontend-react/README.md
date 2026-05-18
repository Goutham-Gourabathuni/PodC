# PodC React Frontend

React + Tailwind replacement for the original Streamlit UI.

## Local development

```bash
cd frontend-react
npm install
copy .env.example .env
npm run dev
```

The frontend reads the backend URL from:

```bash
VITE_API_BASE_URL=https://voltrax123-podc-backend.hf.space
```

For a deployed website, set `VITE_API_BASE_URL` to the public HuggingFace backend URL.

## Production build

```bash
npm run build
```

Deploy the generated `dist/` folder to any static host.
