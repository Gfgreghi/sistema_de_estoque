from fastapi import Depends, HTTPException
from sqlalchemy.orm import sessionmaker, Session
from app.models import Usuario
from app.core.config import settings
from app.core.security import oauth2_schema, PERMISSIONS
from app.core.db import db
from jose import jwt, JWTError
from email_validator import validate_email, EmailNotValidError
from typing import Annotated
def get_db():
    try:
        Sessionlocal = sessionmaker(bind=db)
        session = Sessionlocal()
        yield session
    finally:
        session.close()
    return session
SessionDep = Annotated[Session,Depends(get_db)]
#get current_user
def current_user(user_id: int, session: SessionDep):
        user = session.query(Usuario).filter(Usuario.id==user_id).first()
        if not user:
            raise HTTPException(status_code=401,detail="Acesso invalido")
        return user
#get 
tokenDep = Annotated[str,Depends(oauth2_schema)]
def decode_token(token: tokenDep):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    except JWTError:
        raise HTTPException(status_code=401,detail="Acesso negado, verifique a validade do token")

    return payload
def verify_token(token: tokenDep, session: SessionDep):
        user_id = decode_token(token).get("sub")
        user = current_user(user_id,session)
        return user
def validate_token_type(expected_type: str, token: tokenDep):
    #decodifica o token
    token_data = decode_token(token)
    #verifica se o token bate com o tipo necessario
    token_type = token_data.get("type")
    if not token_type == expected_type:
        raise HTTPException(status_code=401,detail=f"tipo de token invalido, por favor tente um token do tipo {expected_type}")
    return True
UsuarioDep = Annotated[Usuario,Depends(verify_token)]

def verify_email(email: str):
    try:
        email_validado = validate_email(email,check_deliverability=True)
        return email_validado.normalized
    except EmailNotValidError:
        raise HTTPException(status_code=400,detail="email invalido")
#retorna o cargo de um usuarrio
def get_role(user_id: int, session: SessionDep):
    user_role = session.query(Usuario.role).filter(Usuario.id==user_id).scalar()
    if not user_role:
        raise HTTPException(status_code=401,detail="Usuario inexistente")
    return user_role
#verifica se determinado cargo tem tal permissão
def has_permission(user_id: int,required_permission: str,session: SessionDep):
    role = get_role(user_id,session)
    if role not in PERMISSIONS:
        raise HTTPException(status_code=400,detail="cargo inexistente")
    role_permission = PERMISSIONS[role]
    return "*" in role_permission or required_permission in role_permission
def require_permission(user_id: int, required_permission: str, session: SessionDep):
    if not has_permission(user_id,required_permission,session):
        raise HTTPException(status_code=403,detail="Não autorizado")
    return True
