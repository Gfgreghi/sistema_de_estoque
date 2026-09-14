from fastapi import Depends, HTTPException
from sqlalchemy.orm import sessionmaker, Session
from models import db, Usuario
from main import oauth2_schema, SECRET_KEY, ALGORITHM
from jose import jwt, JWTError

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