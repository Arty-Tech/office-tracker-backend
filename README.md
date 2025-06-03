# OFFICE TRACKER – Backend

Questo modulo rappresenta il backend del sistema OFFICE TRACKER.

## Stack Tecnologico

- **Framework:** FastAPI (asincrono, prestazioni elevate, OpenAPI integrata)
- **ORM:** SQLAlchemy (+ Alembic per le migrazioni)
- **Validazione:** Pydantic
- **Autenticazione:** fastapi-jwt-auth (JWT)
- **Database:**
  - PostgreSQL (produzione)
  - SQLite (sviluppo locale)
- **Test:** pytest, pytest-asyncio
- **Docker:** Dockerfile, docker-compose.yml
- **CI/CD:** GitHub Actions

## Installazione

1. Clona il repository principale e accedi alla cartella backend:
   ```bash
   git clone <repo-url>
   cd OFFICE TRACKER/backend
   ```
2. Installa le dipendenze:
   ```bash
   pip install -r requirements.txt
   ```
3. Configura le variabili d'ambiente (vedi `.env.example`)

## Avvio

- Avvio locale:
  ```bash
  uvicorn main:app --reload
  ```
- Avvio con Docker:
  ```bash
  docker-compose up --build
  ```

## Testing

```bash
pytest
```

## Documentazione API

La documentazione OpenAPI/Swagger è disponibile su `/docs` a server avviato.

## Struttura del progetto

- `main.py`: entrypoint FastAPI
- `models/`, `schemas/`, `routes/`: organizzazione del codice
- `alembic/`: migrazioni database

## Contribuire

1. Fai fork del progetto
2. Crea una branch descrittiva (`feature/descrizione`)
3. Fai una pull request

## Licenza

[MIT](../LICENSE)
