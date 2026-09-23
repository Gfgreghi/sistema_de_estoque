from .config import settings
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app.models import Usuario
oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/signin")
bcrypt_context = CryptContext(schemes=["bcrypt"],deprecated=["auto"])
def criar_token(id_usuario,tipo="access_token",duracao_token=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)):
    if tipo == "refresh_token":
        duracao_token= timedelta(days=7)
    data_expiracao =datetime.now(timezone.utc) + duracao_token
    dic_info = {"sub": str(id_usuario), "exp": data_expiracao, "type": tipo}
    jwt_codificado = jwt.encode(dic_info, settings.SECRET_KEY,settings.ALGORITHM)
    token = jwt_codificado
    return token

def autenticar_usuario(email,senha,session):
    usuario = session.query(Usuario).filter(Usuario.email==email).first()
    if not usuario:
        return False
    elif not bcrypt_context.verify(senha,usuario.senha):
        return False
    return usuario

def password_hash(password):
    passwordhash = bcrypt_context.hash(password)