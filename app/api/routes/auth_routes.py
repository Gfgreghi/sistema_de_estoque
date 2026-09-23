from fastapi import APIRouter, Depends, HTTPException
from app.schemas.entry import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session
from app.api.dependencies import get_db, verify_token, validar_email
from app.models import Usuario
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
async def signup(usuario_schema: UsuarioSchema, session: Session = Depends(get_db)):
    email_validado = validar_email(usuario_schema.email)
    usuario = session.query(Usuario).filter(Usuario.email==email_validado).first()
    if usuario:
        raise HTTPException(status_code=400,detail="email ja cadastrado")
    else:
        senha_criptografada = password_hash(usuario_schema.senha)
        novo_usuario = Usuario(usuario_schema.nome,email_validado,senha_criptografada,usuario_schema.ativo,usuario_schema.admin)
        session.add(novo_usuario)
        session.commit()
        return{
            "mensagem": f"usuario {usuario_schema.nome} cadastrado com sucesso"
        }
@auth_router.post("/signin")
async def signin(login_schema: LoginSchema, session: Session = Depends(get_db)):
    usuario = autenticar_usuario(login_schema.email,login_schema.senha,session)
    if not usuario:
        raise HTTPException(status_code=400,detail="usuario não encontrado ou credenciais invalidas")
    else:
        acess_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id,"refresh_token")
        return {
            "acess_token": acess_token,
            "refresh_token": refresh_token
        }
@auth_router.post("/refresh")
async def use_refresh_token(usuario: Usuario = Depends(verify_token("refresh_token"))):
    access_token = criar_token(usuario.id)
    return {
                "access_token": access_token,
                "token_type": "Bearer"
            }