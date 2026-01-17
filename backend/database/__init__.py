from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
import os
from typing import Generator

# DATABASE_URL should be provided by Replit PostgreSQL integration
# Example: postgresql://user:password@host:port/dbname
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

if not SQLALCHEMY_DATABASE_URL:
    # Fallback for development if no DB is provisioned yet
    SQLALCHEMY_DATABASE_URL = "sqlite:///./podcast_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # connect_args={"check_same_thread": False} only needed for SQLite
    connect_args={"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[Session, None, None]:
    """
    Dependency for getting a database session.
    Used in FastAPI route dependencies.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Initializes the database by creating all tables.
    """
    from backend.models import Base, User
    Base.metadata.create_all(bind=engine)
    
    # Seed default user
    db = SessionLocal()
    try:
        if not db.query(User).first():
            default_user = User(email="test@example.com", password_hash="dummyhash")
            db.add(default_user)
            db.commit()
    finally:
        db.close()
