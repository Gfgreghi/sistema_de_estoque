from fastapi import APIRouter, Depends, HTTPException
from schemas import UsuarioSchema
from sqlalchemy.orm import Session
from dependencies import get_db
from models import Usuario
from main import bcrypt_context
auth_router = APIRouter(prefix="/auth",tags=["auth"])

@auth_router.get("/")
async def auth():
    return{
        "mensagem": "bem vindo a rota de autenticação"
    }
@auth_router.post("/signup")
async def signup(usuario_schema: UsuarioSchema, session: Session = Depends(get_db)):
    usuario = session.query(Usuario).filter(Usuario.email==usuario_schema.email).first()
    if usuario:
        raise HTTPException(status_code=400,detail="usuario ja existente")
    else:
        senha_criptografada = bcrypt_context.hash(usuario_schema.senha)
        novo_usuario = Usuario(usuario_schema.nome,usuario_schema.email,senha_criptografada,usuario_schema.ativo,usuario_schema.admin)
        session.add(novo_usuario)
        session.commit()
        return{
            "mensagem": f"usuario {usuario_schema.nome} cadastrado com sucesso"
        }