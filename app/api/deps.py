from fastapi import Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession

# Qui importiamo get_db dal file corretto (session.py), non da deps.py stesso
from app.db.session import get_db
from app.crud.user import crud_user

async def get_current_user(Authorize: AuthJWT = Depends(), db: AsyncSession = Depends(get_db)):
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Non autenticato")
    user_id = Authorize.get_jwt_subject()
    user = await crud_user.get(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utente non trovato")
    return user