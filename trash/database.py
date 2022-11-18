from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()
path = os.getenv('SQL_DATABASE_PATH')
engine = create_engine(path)
Session = sessionmaker(bind=engine)
Base = declarative_base()


def create_session():
    Session = sessionmaker(bind=engine)

    return Session


def create_db():
    Base.metadata.create_all(engine)
