# backend/app/db/base.py

from sqlalchemy.ext.declarative import declarative_base

# Creiamo l'istanza di Base che verrà ereditata da tutti i modelli
Base = declarative_base()
