from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey, VARCHAR, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship
from app.core.db import Base
class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column("id", Integer, primary_key=True,autoincrement=True,nullable=False)
    nome = Column("nome",String,nullable=False)
    email= Column("email",String,nullable=False)
    senha = Column("senha",String,nullable=False)
    ativo = Column("ativo", Boolean)
    admin = Column("admin", Boolean,default=False)
    def __init__(self, nome, email, senha, ativo=True,admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin
class Item(Base):
    __tablename__ = "itens"
    id = Column("id", Integer, primary_key=True,autoincrement=True,nullable=False)
    nome = Column("nome",String,nullable=False)
    bar_code = Column("barcode",VARCHAR(length=13))
    preco = Column("preco",Float)
    preco_promocional = Column("preco_promocional",Float)
    quantidade = Column("quantidade",Integer)
    corredores = relationship("Corredor",secondary="itens_corredores",back_populates="itens")
    def __init__(self, nome, quantidade,barcode, armazenamento=False,preco=0):
        self.nome = nome
        self.bar_code = barcode
        self.preco = preco
        self.quantidade = quantidade
        self.armazenamento = armazenamento
class ItemCorredor(Base):
    __tablename__ = "itens_corredores"

    id = Column("id",Integer,primary_key=True,autoincrement=True,nullable=False)
    item_id = Column("item_id",ForeignKey("itens.id"),nullable=False)
    corredor_id = Column("corredor_id",ForeignKey("corredores.id"),nullable=False)
    quantidade_corredor = Column("quantidade_corredor",Integer)
    __table_args__ = (
        UniqueConstraint(
            "item_id",
            "corredor_id",
            name="uq_item_estoque"
            ),
        )
    def __init__(self,item_id,corredor_id,quantidade=1):
        self.item_id = item_id
        self.corredor_id = corredor_id
        self.quantidade_corredor = quantidade
class Corredor(Base):
    __tablename__ = "corredores"

    id = Column("id", Integer, primary_key=True,autoincrement=True,nullable=False)
    nome = Column("nome",String)
    categoria = Column("categoria",String)
    coluna = Column("coluna",Integer,nullable=False)
    linha = Column("linha",Integer,nullable=False)
    itens = relationship("Item",secondary="itens_corredores",back_populates="corredores")
    def __init__(self,nome,categoria,coluna,linha):
        self.nome = nome
        self.categoria = categoria
        self.coluna = coluna
        self.linha = linha