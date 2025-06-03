from fastapi import FastAPI, Depends
from fastapi_jwt_auth import AuthJWT

from app.core.config import settings
from app.api.endpoints import auth, schedules, timesheet, reports, timer
from app.api.deps import get_current_user

app = FastAPI(title=settings.PROJECT_NAME)


# Configurazione di FastAPI-JWT-Auth per caricare i settings
@AuthJWT.load_config
def get_jwt_config():
    return settings


# Endpoint pubblici per autenticazione
app.include_router(auth.router)

# Endpoint protetti (richiedono JWT valido)
app.include_router(
    schedules.router,
    dependencies=[Depends(get_current_user)]
)
app.include_router(
    timesheet.router,
    dependencies=[Depends(get_current_user)]
)
app.include_router(
    reports.router,
    dependencies=[Depends(get_current_user)]
)
app.include_router(
    timer.router,
    dependencies=[Depends(get_current_user)]
)
