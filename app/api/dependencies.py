from fastapi import Depends, HTTPException
from sqlalchemy.orm import sessionmaker, Session
from app.models import Usuario
from app.core.config import settings
from app.core.security import oauth2_schema
from app.core.db import db
from jose import jwt, JWTError
from email_validator import validate_email, EmailNotValidError
def get_db():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()
    return session
#get current_user
#get 

def verify_token(tipo_esperado: str = "access_token"):
        def dependency(token: str = Depends(oauth2_schema), session: Session = Depends(get_db)):
            try:
                dict_info = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
                id_usuario = dict_info.get("sub")
                tipo_token = dict_info.get("type")
                if tipo_token != tipo_esperado:
                    raise HTTPException(status_code=401,detail=f"tipo de token invalido, para esse endpoint utilize um token do tipo {tipo_esperado}")
            except JWTError:
                raise HTTPException(status_code=401,detail="Acesso negado, verifique a validade do token")
            usuario = session.query(Usuario).filter(Usuario.id==id_usuario).first()
            if not usuario:
                raise HTTPException(status_code=401,detail="Acesso invalido")
            return usuario
        return dependency
def validar_email(email: str):
    try:
        email_validado = validate_email(email,check_deliverability=True)
        return email_validado.normalized
    except EmailNotValidError:
        raise HTTPException(status_code=400,detail="email invalido")