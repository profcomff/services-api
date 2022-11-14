from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import psycopg2

DATABASE_NAME = 'buttons.sqlite'
engine = create_engine(f'postgresql://postgres:123@localhost:5432/Profcom')
# engine = create_engine(f'sqlite:///{DATABASE_NAME}')
Session = sessionmaker(bind=engine)

Base = declarative_base()


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


def create_session():
    Session = sessionmaker(bind=engine)

    return Session


def create_db():
    Base.metadata.create_all(engine)
