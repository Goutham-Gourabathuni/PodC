[!PodC-banner](images/PodC%20-%20banner.png)

## Overview

This is a podcast summarization application with a hybrid architecture: a **Python/FastAPI backend** for AI/ML processing and a **React/TypeScript frontend** for the user interface. The application allows users to submit podcasts (via URL or upload), which are then transcribed and summarized using machine learning pipelines.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite with custom configuration
- **Routing**: Wouter (lightweight React router)
- **State Management**: TanStack React Query for server state
- **UI Components**: shadcn/ui component library built on Radix UI primitives
- **Styling**: Tailwind CSS with CSS variables for theming (light/dark mode support)
- **Path Aliases**: `@/` maps to `client/src/`, `@shared/` maps to `shared/`

### Backend Architecture
- **Primary API**: Python FastAPI (runs on port 5000 via uvicorn)
- **Secondary Server**: Express.js/Node.js server exists for static file serving and potential future routes
- **API Pattern**: RESTful endpoints organized by domain (`/auth`, `/pipeline`)
- **Database ORM**: SQLAlchemy (Python) for the main app, Drizzle ORM (TypeScript) for shared schema definitions

### Data Storage
- **Database**: PostgreSQL (configured via `DATABASE_URL` environment variable)
- **Schema Management**: 
  - Python SQLAlchemy models in `backend/models/`
  - TypeScript Drizzle schema in `shared/schema.ts` for type sharing
- **Migrations**: Drizzle Kit for schema migrations (`drizzle-kit push`)
- **Fallback**: SQLite for local development if no PostgreSQL URL provided

### Key Data Models
- **User**: Authentication with email/password hash
- **Podcast**: Audio source metadata (URL or upload), linked to user
- **Result**: Processing output (transcript, topics, summary, PDF/DOC paths)

### Processing Pipeline
The `backend/pipeline/` module handles:
1. Audio ingestion (URL fetch or file upload)
2. Transcription (using faster-whisper)
3. Topic extraction (NLP via spacy, nltk)
4. Summarization
5. Document generation (PDF via reportlab, DOCX via python-docx)

### Authentication
- Password hashing with passlib/bcrypt
- JWT token generation with python-jose
- Placeholder for Replit Auth/OAuth integration

## External Dependencies

### AI/ML Libraries (Python)
- **faster-whisper**: Audio transcription
- **spacy**: NLP processing
- **nltk**: Natural language toolkit
- **scikit-learn**: Machine learning utilities
- **librosa/pydub**: Audio processing

### Document Generation (Python)
- **python-docx**: Word document generation
- **reportlab**: PDF generation

### Database
- **PostgreSQL**: Primary database (requires `DATABASE_URL` environment variable)
- **psycopg2-binary**: PostgreSQL adapter for Python
- **SQLAlchemy**: Python ORM
- **drizzle-orm**: TypeScript ORM for shared types

### Frontend Libraries
- **@tanstack/react-query**: Data fetching and caching
- **@radix-ui/***: Accessible UI primitives
- **wouter**: Client-side routing
- **class-variance-authority**: Component variant styling

### Development Commands
- `npm run dev`: Start FastAPI backend with hot reload
- `npm run build`: Build frontend and bundle server
- `npm run db:push`: Push database schema changes