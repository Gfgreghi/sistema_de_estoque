from sqlalchemy.orm import sessionmaker, session
from models import db

def get_db():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()
    return session