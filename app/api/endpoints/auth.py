from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.hash import bcrypt
from fastapi_jwt_auth import AuthJWT

from app import crud, schemas
from app.api.deps import get_db
from app.core.security import create_access_token

router = APIRouter(tags=["auth"], prefix="/auth")


@router.post("/register", response_model=schemas.user.UserRead, status_code=status.HTTP_201_CREATED)
async def register(user_in: schemas.user.UserCreate, db: AsyncSession = Depends(get_db)):
    existing = await crud.user.get_by_email(db, user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email già registrata")
    hashed = bcrypt.hash(user_in.password)
    user = await crud.user.create(db, user_in, hashed)
    return user


@router.post("/login", response_model=schemas.user.Token)
async def login(user_in: schemas.user.UserLogin, Authorize: AuthJWT = Depends(), db: AsyncSession = Depends(get_db)):
    user = await crud.user.get_by_email(db, user_in.email)
    if not user or not bcrypt.verify(user_in.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenziali non valide")
    access_token = create_access_token(subject=str(user.id))
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=schemas.user.UserRead)
async def me(Authorize: AuthJWT = Depends(), db: AsyncSession = Depends(get_db)):
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    user = await crud.user.get(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utente non trovato")
    return user
