from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.future import select

from app.core.database import SessionLocal
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.config import settings
from app.models.sql import User
from app.schemas.user import UserCreate, UserOut, Token

router = APIRouter()

@router.post("/signup", response_model=UserOut)
async def signup(user_in: UserCreate):
    async with SessionLocal() as session:
        # Check if user exists
        result = await session.execute(select(User).where(User.email == user_in.email))
        if result.scalars().first():
            raise HTTPException(
                status_code=400,
                detail="The user with this email already exists in the system."
            )
        
        user = User(
            email=user_in.email,
            full_name=user_in.full_name,
            hashed_password=get_password_hash(user_in.password)
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    async with SessionLocal() as session:
        result = await session.execute(select(User).where(User.email == form_data.username))
        user = result.scalars().first()

        if not user or not verify_password(form_data.password, user.hashed_password): 
             raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
