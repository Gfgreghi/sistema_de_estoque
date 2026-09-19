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
    preco: float
    quantidade: int

class Config:
    from_attributes = True

class ResponseCorredorSchema(BaseModel):
    id: int
    nome: str
    categoria: str
    coluna: int
    linha: int
    itens: List[ItemSchema]

class Config:
    from_attributes = True

class ResponseCorredorUpdateSchema(BaseModel):
    mensagem: str
    campos_alterados: List[str]
    corredor: ResponseCorredorSchema

class CorredorUpdateSchema(BaseModel):
    nome: Optional[str] = None
    categoria: Optional[str] = None
    coluna: Optional[int] = None
    linha: Optional[int] = None

class Config:
    from_attributes = True
