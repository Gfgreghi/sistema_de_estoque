from fastapi import APIRouter, Depends, HTTPException
from schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session
from dependencies import get_db, verify_token, validar_email
from models import Usuario
from main import bcrypt_context, SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
auth_router = APIRouter(prefix="/auth",tags=["auth"])
def criar_token(id_usuario,duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    data_expiracao =datetime.now(timezone.utc) + duracao_token
    dic_info = {"sub": str(id_usuario), "exp": data_expiracao}
    jwt_codificado = jwt.encode(dic_info, SECRET_KEY,ALGORITHM)
    token = jwt_codificado
    return token
def autenticar_usuario(email,senha,session):
    usuario = session.query(Usuario).filter(Usuario.email==email).first()
    if not usuario:
        return False
    elif not bcrypt_context.verify(senha,usuario.senha):
        return False
    return usuario

@auth_router.get("/")
async def auth():
    return{
        "mensagem": "bem vindo a rota de autenticação"
    }
@auth_router.post("/signup")
async def signup(usuario_schema: UsuarioSchema, session: Session = Depends(get_db),usuario: Usuario = Depends(verify_token)):
    email_validado = validar_email(usuario_schema.email)
    usuario = session.query(Usuario).filter(Usuario.email==email_validado).first()
    if usuario:
        raise HTTPException(status_code=400,detail="email ja cadastrado")
    else:
        senha_criptografada = bcrypt_context.hash(usuario_schema.senha)
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
        refresh_token = criar_token(usuario.id,timedelta(days=7))
        return {
            "acess_token": acess_token,
            "refresh_token": refresh_token
        }
@auth_router.get("/refresh")
async def use_refresh_token(usuario: Usuario = Depends(verify_token)):
    access_token = criar_token(usuario.id)
    return {
                "access_token": access_token,
                "token_type": "Bearer"
            }