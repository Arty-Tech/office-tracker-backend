from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT

from app.core.config import settings
from app.api.endpoints import auth, schedules, timesheet, reports, timer
from app.api.deps import get_current_user

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API per il tracker di orari e turni lavorativi",
    version="0.0.1",
)

# Security scheme per Swagger (Bearer token)
bearer_scheme = HTTPBearer(
    description="Inserisci qui il tuo token JWT con il prefisso `Bearer `"
)

# Configurazione di FastAPI-JWT-Auth per caricare i settings
@AuthJWT.load_config
def get_jwt_config():
    return settings


# -------------------------------------------------------------------------
# 1. Endpoint pubblici per autenticazione (non richiedono token)
# -------------------------------------------------------------------------
app.include_router(auth.router)


# -------------------------------------------------------------------------
# 2. Endpoint protetti (richiedono JWT valido + mostrano “Authorize” in /docs)
#    – Aggiungiamo HTTPBearer come dipendenza, poi get_current_user per la logica JWT
# -------------------------------------------------------------------------
app.include_router(
    schedules.router,
    dependencies=[Depends(bearer_scheme), Depends(get_current_user)],
)
app.include_router(
    timesheet.router,
    dependencies=[Depends(bearer_scheme), Depends(get_current_user)],
)
app.include_router(
    reports.router,
    dependencies=[Depends(bearer_scheme), Depends(get_current_user)],
)
app.include_router(
    timer.router,
    dependencies=[Depends(bearer_scheme), Depends(get_current_user)],
)
