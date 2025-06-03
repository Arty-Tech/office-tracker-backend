from fastapi import Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.api.deps import get_db


async def get_current_user(Authorize: AuthJWT = Depends(), db: AsyncSession = Depends(get_db)):
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Non autenticato")
    user_id = Authorize.get_jwt_subject()
    user = await crud.user.get(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utente non trovato")
    return user
