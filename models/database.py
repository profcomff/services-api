from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import psycopg2

DATABASE_NAME = 'buttons.db'
engine = create_engine(f'postgresql+psycopg2://postgres:123@localhost:5432/{DATABASE_NAME}')
Session = sessionmaker(bind=engine)

Base = declarative_base()

def create_db():
    Base.metadata.create_all(engine)
