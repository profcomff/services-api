from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from fastapi import FastAPI
from dotenv import load_dotenv
import os

db = None
load_dotenv()
login = os.getenv('SQL_LOGIN')
password = os.getenv('SQL_PASSWORD')
host = os.getenv('SQL_HOST')
port = int(os.getenv('SQL_PORT'))
tablespace = os.getenv('SQL_TABLESPACE')
path = f'postgresql://{login}:{password}@{host}:{port}/{tablespace}'
engine = create_engine(path)
Session = sessionmaker(bind=engine)
Base = declarative_base()
Base.metadata.create_all(bind=create_engine(path))
app = FastAPI()


def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()
