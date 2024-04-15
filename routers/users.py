import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from database import SessionLocal
from models import User
import jwt
from dotenv import load_dotenv

load_dotenv()
AUTH_TOKEN_SECRET = os.environ.get("AUTH_TOKEN_SECRET")
JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM")

router = APIRouter()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register/")
def create_user(email: str, password: str):
    db = SessionLocal()
    try:
        # Check if the username already exists
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already exists")
        # Hash the password
        hashed_password = pwd_context.hash(password)
        # Create the user
        user = User(email=email, password=hashed_password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    finally:
        db.close()


@router.get("/users/{user_id}")
def get_user(user_id: int):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    finally:
        db.close()


@router.post("/login/")
def login_user(email: str, password: str):
    db = SessionLocal()
    try:

        # Retrieve user from database
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise HTTPException(status_code=400, detail="Invalid email")

        # Check password
        if not pwd_context.verify(password, user.password):
            raise HTTPException(status_code=400, detail="Invalid password")

        access_token = email

        return {"access_token": access_token, "token_type": "bearer"}
    finally:
        db.close()
