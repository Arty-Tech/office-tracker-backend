from fastapi import FastAPI
from fastapi_jwt_auth import AuthJWT
from app.core.config import settings
from app.api.endpoints import auth, schedules, timesheets, reports, timer

app = FastAPI(title=settings.PROJECT_NAME)


@AuthJWT.load_config
def get_jwt_config():
    return settings


app.include_router(auth.router)
app.include_router(schedules.router, dependencies=[Depends(get_current_user)])
app.include_router(timesheets.router, dependencies=[Depends(get_current_user)])
app.include_router(reports.router, dependencies=[Depends(get_current_user)])
app.include_router(timer.router, dependencies=[Depends(get_current_user)])
