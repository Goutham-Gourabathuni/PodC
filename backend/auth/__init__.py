"""
Authentication module.
Handles user authentication, JWT token generation, and verification.
Integration with Replit Auth or OAuth providers should be implemented here.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import User
from backend.auth.jwt import create_access_token
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["Authentication"])

class LoginRequest(BaseModel):
    email: str

@router.post("/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email).first()

    if not user:
        user = User(
            username=req.email,   # ✅ FIX
            email=req.email,
            password_hash="dummyhash"
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    token = create_access_token({"user_id": user.id})
    return {"access_token": token}
