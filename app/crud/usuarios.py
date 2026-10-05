from app.models import Usuario
from app.api.dependencies import SessionDep
from app.schemas.entry import UserCreate
from fastapi import HTTPException
#criar usuario
def create(session: SessionDep,nome: str,email: str,senha: str,ativo: bool=True,admin: str="user"):
    if  session.query(Usuario).filter(Usuario.email==email).first():
        raise HTTPException(status_code=400,detail="Usuario já existe")
    novo_usuario = Usuario(nome,email,senha,ativo,admin)
    session.add(novo_usuario)
    session.commit()
    return novo_usuario
#ver usuario
def read(user_id,session: SessionDep):
    usuario = session.query(Usuario).filter(user_id==Usuario.id).first
    if not usuario:
        raise HTTPException(status_code=400,detail="usuario não encontrado ou credenciais invalidas")
    return usuario
#editar usuario

#apagar usuario
