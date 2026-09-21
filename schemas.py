from pydantic import BaseModel
from typing import Optional, List
#schemas de entrada de dados
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
#schemas de entrada de dados de atualização
class CorredorUpdateSchema(BaseModel):
    nome: Optional[str] = None
    categoria: Optional[str] = None
    coluna: Optional[int] = None
    linha: Optional[int] = None

class Config:
    from_attributes = True

class ItemUpdateSchema(BaseModel):
    nome: Optional[str]
    bar_code: Optional[int]
    preco: Optional[float]
    quantidade: Optional[int]

class Config:
    from_attributes = True
#schemas de saida de dados
class ResponseCorredorSchema(BaseModel):
    id: int
    nome: str
    categoria: str
    coluna: int
    linha: int
    itens: List[ItemSchema]

class Config:
    from_attributes = True
class ResponseItemSchema(BaseModel):
    id: int
    nome: str
    bar_code: int
    preco: float
    quantidade: int

class Config:
    from_attributes = True

#schema de saida de dados de atualização
class ResponseCorredorUpdateSchema(BaseModel):
    mensagem: str
    campos_alterados: List[str]
    corredor: ResponseCorredorSchema

class ResponseItemUpdateSchema(BaseModel):
    mensagem: str
    campos_alterados: List[str]
    item: ResponseItemSchema
