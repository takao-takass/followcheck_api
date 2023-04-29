import datetime
import json
from fastapi import FastAPI, Response
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

app = FastAPI()

class Config(BaseModel):
    connection_string: str

class Config:
    def __init__(self, connection_string):
        self.connection_string = connection_string

# configの読み込み
with open("config.json") as f:
    loaded_config = json.load(f)
    config = Config(**loaded_config)

database_url = config.connection_string
engine = create_engine(database_url)

Base = declarative_base()

class ServiceUsers(Base):
    __tablename__ = "service_users"

    service_user_id = Column(String(255), primary_key=True)
    name = Column(String(255))
    mailaddress = Column(String(255))
    password = Column(String(255))
    deleted = Column(Integer)

# テーブルの作成（必要に応じて）
# Base.metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@app.get("/test/tweets")
def get_tweets():

    session = SessionLocal()
    service_users = session.query(ServiceUsers).all()
    session.close()

    for service_user in service_users:
        print(f"ID: {service_user.service_user_id}, Name: {service_user.name}, MAIL: {service_user.mailaddress}")

    return {"tweets": "tweets"}

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
