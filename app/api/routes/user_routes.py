from fastapi import APIRouter, Depends, HTTPException
from app.schemas.entry import UserCreate, AdminUserCreate, LoginSchema
from app.api.dependencies import  verify_email, SessionDep, UsuarioDep, require_permission
from app.schemas.update import UsuarioUpdateSchema
from app.models import Usuario
import app.crud.usuarios as user
from app.core.security import (
    password_hash,
    autenticar_usuario,
    criar_token
)
users_router = APIRouter(prefix="/users",tags=["users"])

@users_router.get("/")
async def users():
    return{
        "mensagem": "bem vindo a rota de usuarios"
    }
@users_router.patch("/user/{user_id}")
async def edit_user(usuario_update_schema: UsuarioUpdateSchema,user_id: int,usuario: UsuarioDep,session: SessionDep):
    if usuario.id != user_id:
        require_permission(usuario.role,"edit_user",session)
    user_update = user.update(user_id,usuario_update_schema,session)
    users = user_update["usuario"]
    return{
        "mensagem": f"informações do user {users.id} alterado com sucesso",
        "campos_alterados": user_update["campos_alterados"],
        "corredor": users
    }