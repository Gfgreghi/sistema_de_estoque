from fastapi import FastAPI
from app.core.init_db import init_db
app = FastAPI()
init_db()
from app.api.routes.auth_routes import auth_router
from app.api.routes.storage_routes import storage_router
from app.api.routes.item_routes import item_router
from app.api.routes.user_routes import users_router
app.include_router(auth_router)
app.include_router(storage_router)
app.include_router(item_router)
app.include_router(users_router)