#!/usr/bin/env python3
# console/init.py

import os
import uuid
import click

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passlib.hash import bcrypt

# IMPORTA TUTTI I MODELLI PRIMA di toccare la sessione:
from app.models.user import User
from app.models.workday_config import WorkDayConfig
from app.models.time_entry import TimeEntry
from app.models.punch import Punch

@click.group(help="⭑ Comandi di inizializzazione (init) ⭑")
def init():
    """
    Gruppo di comandi per l’inizializzazione (es. creazione admin).
    """
    ...


@init.command("create_admin")
@click.option(
    "--email",
    default="admin@officetracker.org",
    show_default=True,
    help="Email dell’utente admin da creare",
)
@click.option(
    "--password",
    default="AdminPassword123!",
    show_default=True,
    help="Password dell’utente admin da creare",
)
def create_admin(email: str, password: str):
    """
    Crea un utente “admin” di default nel database.
    """
    # Ottieni DATABASE_URL dall’ambiente
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        click.echo("⛔ ERRORE: variabile d’ambiente DATABASE_URL non trovata.")
        return

    # Trasforma l’URL async in un URL sync per psycopg2
    sync_url = db_url.replace("postgresql+asyncpg", "postgresql+psycopg2")

    # Crea l’engine e la Session sincrona
    engine = create_engine(sync_url, echo=False, future=True)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    session = SessionLocal()
    try:
        # Controlla se esiste già un utente con questa email
        existing = session.query(User).filter(User.email == email).first()
        if existing:
            click.echo(f"ℹ️  Utente con email '{email}' è già presente.")
            return

        # Hash della password
        hashed_pw = bcrypt.hash(password)

        # Crea il nuovo oggetto User (con UUID generato)
        new_admin = User(
            id=uuid.uuid4(),
            email=email,
            hashed_password=hashed_pw,
            nome="Admin",
            preferences={
                "workDuration": 30,
                "breakDuration": 5,
                "soundUrl": "/audio/bell.mp3"
            },
        )
        session.add(new_admin)
        session.commit()
        click.echo(f"✅ Utente admin '{email}' creato con successo.")
    except Exception as e:
        session.rollback()
        click.echo(f"❌ Errore durante la creazione dell’admin: {e}")
    finally:
        session.close()
