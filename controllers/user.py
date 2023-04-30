from fastapi import APIRouter
from logics.user import get_service_users as get_service_users_logic
from sqlalchemy import create_engine
from configurations.config import load_config

config = load_config()
database_url = config.connection_string
engine = create_engine(database_url)

router = APIRouter()

@router.get("/user/service_users")
async def get_service_users():
    return get_service_users_logic(engine)

def include_router(app):
    app.include_router(router)