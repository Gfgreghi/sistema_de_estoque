from fastapi import APIRouter, Depends, HTTPException
from app.schemas.entry import UserCreate, AdminUserCreate, LoginSchema
from app.schemas.response import ResponseUserUpdateSchema, ResponseUserSchema
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

@users_router.get("/user/{user_id}",response_model=ResponseUserSchema)
async def users(user_id: int,session: SessionDep, usuario: UsuarioDep):
    if not user_id == usuario.id:
        require_permission(usuario.role,"view_another_user",session)
    users = user.read(user_id,session)
    return users
@users_router.patch("/user/{user_id}", response_model=ResponseUserUpdateSchema)
async def edit_user(usuario_update_schema: UsuarioUpdateSchema,user_id: int,usuario: UsuarioDep,session: SessionDep):
    if usuario.id != user_id:
        require_permission(usuario.role,"edit_user",session)
    user_update = user.update(usuario_update_schema,user_id,session,role = usuario.role)
    users = user_update["usuario"]
    return{
        "mensagem": f"informações do user {users.id} alterado com sucesso",
        "campos_alterados": user_update["campos_alterados"],
        "usuario": users
    }