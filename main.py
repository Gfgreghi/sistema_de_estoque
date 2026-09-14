from fastapi import FastAPI

app = FastAPI()

from auth_routes import auth_router
from storage_routes import storage_router
app.include_router(auth_router)
app.include_router(storage_router)