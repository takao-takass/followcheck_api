import datetime
import json
from fastapi import FastAPI, Response
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.get("/test/tweets")
def get_tweets():

    config = None
    with open("config.json") as f:
        loaded_config = json.load(f)
        config = Config(**loaded_config)

    if config is None:
        return Response(status_code=400)
    
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

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()

    service_users = session.query(ServiceUsers).all()

    session.close()

    for service_user in service_users:
        print(f"ID: {service_user.service_user_id}, Name: {service_user.name}, MAIL: {service_user.mailaddress}")

    return {"tweets": "tweets"}

# 接続文字列のモデルクラスを定義します。
class Config(BaseModel):
    connection_string: str
