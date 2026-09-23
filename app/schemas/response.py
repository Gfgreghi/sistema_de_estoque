from pydantic import BaseModel
from typing import Optional, List
from .entry import ItemSchema
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

class ResponseCorredorUpdateSchema(BaseModel):
    mensagem: str
    campos_alterados: List[str]
    corredor: ResponseCorredorSchema

class ResponseItemUpdateSchema(BaseModel):
    mensagem: str
    campos_alterados: List[str]
    item: ResponseItemSchema