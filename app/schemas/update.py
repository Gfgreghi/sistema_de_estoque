from pydantic import BaseModel
from typing import Optional, List
from .entry import ItemSchema
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