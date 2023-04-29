from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from config import load_config
from routes import get_tweets

app = FastAPI()

# テーブルの作成（必要に応じて）
# Base.metadata.create_all(engine)

config = load_config()
database_url = config.connection_string
engine = create_engine(database_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@app.get("/test/tweets")
async def get_all_tweets():
    return get_tweets(engine)