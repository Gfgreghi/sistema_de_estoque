from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey, VARCHAR
from sqlalchemy.orm import declarative_base, relationship

#cria a conexão do banco
db = create_engine("sqlite:///banco.db")
#cria a base do banco
Base = declarative_base()

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
    quantidade = Column("quantidade",Integer)
    armazenamento = Column("armazenamento",ForeignKey("estoque.id"),nullable=False)
    def __init__(self, nome, quantidade, armazenamento=False,preco=0):
        self.nome = nome
        self.preco = preco
        self.quantidade = quantidade
        self.armazenamento = armazenamento
class Estoque(Base):
    __tablename__ = "estoque"

    id = Column("id", Integer, primary_key=True,autoincrement=True,nullable=False)
    nome = Column("nome",String)
    categoria = Column("categoria",String)
    coluna = Column("coluna",Integer,nullable=False)
    linha = Column("linha",Integer,nullable=False)
    itens = relationship("Item",cascade="all, delete")
    def __init__(self,nome,categoria,coluna,linha):
        self.nome = nome
        self.categoria = categoria
        self.coluna = coluna
        self.linha = linha