from fastapi import FastAPI

app = FastAPI()

from app.api.routes.auth_routes import auth_router
from app.api.routes.storage_routes import storage_router
app.include_router(auth_router)
app.include_router(storage_router)