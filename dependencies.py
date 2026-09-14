from fastapi import Depends, HTTPException
from sqlalchemy.orm import sessionmaker, Session
from models import db, Usuario
from main import oauth2_schema, SECRET_KEY, ALGORITHM
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
def verify_token(token: str = Depends(oauth2_schema), session: Session = Depends(get_db)):
    try:
        dict_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_usuario = dict_info.get("sub")
    except JWTError:
        raise HTTPException(status_code=401,detail="Acesso negado, verifique a validade do token")
    usuario = session.query(Usuario).filter(Usuario.id==id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=401,detail="Acesso invalido")
    return usuario
def validar_email(email: str):
    try:
        email_validado = validate_email(email,check_deliverability=True)
        return email_validado.normalized
    except EmailNotValidError:
        raise HTTPException(status_code=400,detail="email invalido")