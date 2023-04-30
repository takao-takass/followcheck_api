from fastapi import FastAPI
from configurations.config import load_config
from controllers.user import get_user_router

app = FastAPI()

config = load_config()
user_router = get_user_router(config)
app.include_router(user_router)