from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.entry import UserCreate, AdminUserCreate, LoginSchema
from app.api.dependencies import  verify_email, SessionDep, UsuarioDep, require_permission
from app.models import Usuario
import app.crud.usuarios as user
from app.core.security import (
    password_hash,
    autenticar_usuario,
    criar_token
)
auth_router = APIRouter(prefix="/auth",tags=["auth"])

@auth_router.get("/")
async def auth():
    return{
        "mensagem": "bem vindo a rota de autenticação"
    }
@auth_router.post("/signup")
async def signup(usuario_schema: UserCreate, session: SessionDep):
    email_validado = verify_email(usuario_schema.email)
    senha_criptografada = password_hash(usuario_schema.senha)
    usuario = user.create(session,usuario_schema.nome,email_validado,senha_criptografada)
    return{
            "mensagem": f"usuario {usuario.nome} cadastrado com sucesso"
        }
@auth_router.post("/admin/signup/")
async def signup(usuario_schema: AdminUserCreate, session: SessionDep, usuario: UsuarioDep):
    require_permission(usuario.role,"create_roleduser")
    email_validado = verify_email(usuario_schema.email)
    senha_criptografada = password_hash(usuario_schema.senha)
    usuario = user.create(session,usuario_schema.nome,email_validado,senha_criptografada,usuario_schema.ativo,usuario_schema.role)
    return{
            "mensagem": f"usuario {usuario.nome} cadastrado com sucesso"
        }
@auth_router.patch("/user")
async def edit_user(usuario_update_schema):
    pass
@auth_router.post("/signin")
async def signin(login_schema: LoginSchema, session: SessionDep):
    usuario = autenticar_usuario(login_schema.email,login_schema.senha,session)
    if not usuario:
        raise HTTPException(
            status_code=401,
            detail="Email ou senha inválidos"
        )

@auth_router.post("/signin-form")
async def signin( session: SessionDep,login_schema: OAuth2PasswordRequestForm = Depends()):
    usuario = autenticar_usuario(login_schema.username,login_schema.password,session)
    if not usuario:
        raise HTTPException(
            status_code=401,
            detail="Email ou senha inválidos"
        )
    access_token = criar_token(usuario.id)
    refresh_token = criar_token(usuario.id,"refresh_token")
    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }
@auth_router.post("/refresh")
async def use_refresh_token(usuario: UsuarioDep):
    access_token = criar_token(usuario.id)
    return {
                "access_token": access_token,
                "token_type": "Bearer"
            }