from app.models import Usuario
from app.api.dependencies import SessionDep, require_permission
from app.schemas.entry import UserCreate
from app.schemas.update import UsuarioUpdateSchema, AdminUsuarioUpdateSchema
from app.core.security import password_hash
from fastapi import HTTPException
#criar usuario
def create(session: SessionDep,nome: str,email: str,senha: str,ativo: bool=True,role: str="user"):
    if  session.query(Usuario).filter(Usuario.email==email).first():
        raise HTTPException(status_code=400,detail="Usuario já existe")
    novo_usuario = Usuario(nome,email,senha,ativo,role)
    session.add(novo_usuario)
    session.commit()
    return novo_usuario
#ver usuario
def read(user_id,session: SessionDep):
    usuario = session.query(Usuario).filter(user_id==Usuario.id).first()
    if not usuario:
        raise HTTPException(status_code=400,detail="usuario não encontrado ou credenciais invalidas")
    return usuario
#editar usuario
def update(usuario_update_schema: UsuarioUpdateSchema,user_id:int,session: SessionDep, role: str = "user"):
    user = session.query(Usuario).filter(Usuario.id==user_id).first()
    if not user:
        raise HTTPException(status_code=404,detail="item não cadastrado")
    updated = usuario_update_schema.model_dump(exclude_unset=True)
    campos_alterados = []
    for campo, valor in updated.items():
        if campo == "role":
            require_permission(role,"edit_userrole")
        if campo == "ativo":
            require_permission(role,"edit_useractive")
        if campo == "senha":
            valor = password_hash(valor)
        setattr(user, campo, valor)
        campos_alterados.append(campo)
    session.commit()
    session.refresh(user)
    return {
        "usuario": user, 
        "campos_alterados": campos_alterados
            }
#apagar usuario

#verificar se há usuario
def has_user(session: SessionDep):
    stmt = session.query(Usuario).limit(1)
    return session.scalar(stmt) is not None
#criar usuario sendo admin