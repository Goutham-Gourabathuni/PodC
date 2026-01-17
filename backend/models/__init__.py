from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON, Enum
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func
import enum

Base = declarative_base()

class SourceType(enum.Enum):
    URL = "URL"
    UPLOAD = "UPLOAD"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    podcasts = relationship("Podcast", back_populates="owner")

class Podcast(Base):
    __tablename__ = "podcasts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    source_type = Column(Enum(SourceType), nullable=False)
    audio_path = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="podcasts")
    result = relationship("Result", back_populates="podcast", uselist=False)

class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)
    podcast_id = Column(Integer, ForeignKey("podcasts.id"), unique=True, nullable=False)
    transcript = Column(Text, nullable=True)
    topics = Column(JSON, nullable=True)
    summary = Column(Text, nullable=True)
    pdf_path = Column(String, nullable=True)
    doc_path = Column(String, nullable=True)

    podcast = relationship("Podcast", back_populates="result")
