from .config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

#cria a conexão do banco
db = create_engine(settings.DATABASE_URL)
#cria a base do banco
Base = declarative_base()
