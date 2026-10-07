from app.core.security import password_hash
from app.crud.usuarios import create, has_user
from app.core.db import db
from sqlalchemy.orm import Session
def init_db():
    with Session(db) as session:
        if not has_user(session):
            create( session,
                    nome="admin",
                    email="admin@admin.com",
                    senha=password_hash("admin@123"),
                    ativo=True,
                    role="admin")

        