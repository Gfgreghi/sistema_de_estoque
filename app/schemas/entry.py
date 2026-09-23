from pydantic import BaseModel
from typing import Optional, List

class UsuarioSchema(BaseModel):
    nome: str
    email: str
    senha:str
    ativo: Optional[bool]
    admin: Optional[bool]

class Config:
    from_attributes = True

class LoginSchema(BaseModel):
    email: str
    senha: str

class Config:
    from_attributes = True

class CorredorSchema(BaseModel):
    nome: str
    categoria: str
    coluna: int
    linha: int

class Config:
    from_attributes = True

class ItemSchema(BaseModel):
    nome: str
    bar_code: int
    preco: Optional[float]
    quantidade: int

class Config:
    from_attributes = True

class ItemCorredorSchema(BaseModel):
    item_id: int
    quantidade: Optional[int] = 1
class Config:
    from_attributes = True