import os
import asyncio
import uuid as _uuid
import bcrypt
import sqlalchemy as sa

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# dal tuo progetto:
from app.models.user import User
from app.db.base import Base

def create_admin(email: str = "admin@officetracker.org", password: str = "AdminPassword123!"):
    """
    Crea un utente admin di default con email e password passate come parametri.
    Se esiste già un utente con quell’email, segnala e non fa nulla.
    
    Esempio di uso:
      ./manager.py init create_admin
      └─ usa email e password di default

      ./manager.py init create_admin admin2@example.com SecretPwd
    """
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:p0stgr3s@db/time_tracker_db")

    async def _inner(email_arg: str, password_arg: str):
        # Inizializza il motore asincrono
        engine = create_async_engine(DATABASE_URL, future=True, echo=False)
        AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

        async with AsyncSessionLocal() as session:
            # Verifica se esiste già
            result = await session.execute(sa.select(User).where(User.email == email_arg))
            existing = result.scalars().first()
            if existing:
                print(f"⚠️  Esiste già un utente con email: {existing.email}")
                return

            # Crea hash della password
            salt = bcrypt.gensalt()
            hashed_pw = bcrypt.hashpw(password_arg.encode(), salt).decode()

            # ID fisso per admin (puoi cambiarlo)
            admin_id = _uuid.UUID("11111111-1111-1111-1111-111111111111")
            user = User(
                id=admin_id,
                email=email_arg,
                hashed_password=hashed_pw,
                nome="Administrator",
                preferences={
                    "workDuration": 25,
                    "breakDuration": 5,
                    "soundUrl": "/audio/bell.mp3"
                }
            )
            session.add(user)
            await session.commit()
            print(f"✅ Admin creato: {email_arg}")

    # se sono stati passati 0 argomenti, uso i default; se 2, li sovrascrivo
    args = []
    if len(os.sys.argv) >= 4:
        args = os.sys.argv[3:5]  # email e password
    elif len(os.sys.argv) == 3:
        # nessun parametro extra: uso default
        args = []
    else:
        # se ne passano 1 o >2 → errore di sintassi
        print("Usage: ./manager.py init create_admin [<email> <password>]")
        return

    # Se args è vuoto, chiamare con valori di default
    if args:
        asyncio.run(_inner(args[0], args[1]))
    else:
        asyncio.run(_inner(email, password))
