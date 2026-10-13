from sqlalchemy import Column, String, Integer, Boolean, Float, ForeignKey, VARCHAR, UniqueConstraint
from sqlalchemy.orm import relationship
from app.core.db import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    nome = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    senha = Column(String(255), nullable=False)
    ativo = Column(Boolean, default=True)
    role = Column(String(255), default="User")

    def __init__(self, nome, email, senha, ativo=True, role="User"):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.role = role

class Item(Base):
    __tablename__ = "itens"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    nome = Column(String(255), nullable=False)
    bar_code = Column(VARCHAR(13))
    preco = Column(Float)
    preco_promocional = Column(Float)
    quantidade = Column(Integer)
    
    # CORREÇÃO 2: back_populates mapeado corretamente para a variável da outra classe
    corredores = relationship("Corredor", secondary="itens_corredores", back_populates="itens")

    def __init__(self, nome, quantidade, barcode, armazenamento=False, preco=0):
        self.nome = nome
        self.bar_code = barcode  # Garante o vínculo correto com a coluna ajustada acima
        self.preco = preco
        self.quantidade = quantidade
        self.armazenamento = armazenamento

class ItemCorredor(Base):
    __tablename__ = "itens_corredores"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    item_id = Column(ForeignKey("itens.id"), nullable=False)
    corredor_id = Column(ForeignKey("corredores.id"), nullable=False)
    quantidade_corredor = Column(Integer)

    __table_args__ = (
        UniqueConstraint("item_id", "corredor_id", name="uq_item_estoque"),
    )

    def __init__(self, item_id, corredor_id, quantidade=1):
        self.item_id = item_id
        self.corredor_id = corredor_id
        self.quantidade_corredor = quantidade

class Corredor(Base):
    __tablename__ = "corredores"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    nome = Column(String(255))
    categoria = Column(String(255))
    coluna = Column(Integer, nullable=False)
    linha = Column(Integer, nullable=False)
    
    # CORREÇÃO 2: back_populates mapeado corretamente para a variável da outra classe
    itens = relationship("Item", secondary="itens_corredores", back_populates="corredores")

    def __init__(self, nome, categoria, coluna, linha):
        self.nome = nome
        self.categoria = categoria
        self.coluna = coluna
        self.linha = linha

