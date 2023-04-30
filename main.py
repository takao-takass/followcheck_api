from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from configurations.config import load_config
import controllers.user as user

app = FastAPI()

config = load_config()
database_url = config.connection_string
engine = create_engine(database_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

user.include_router(app)