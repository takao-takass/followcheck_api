from fastapi import APIRouter
from logics.user import fetch_service_users
from sqlalchemy import create_engine

def get_user_router(config):
    database_url = config.connection_string
    engine = create_engine(database_url)

    router = APIRouter()

    @router.get("/user/service_users")
    async def get_service_users():
        return fetch_service_users(engine)

    return router
