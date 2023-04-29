from sqlalchemy.orm import sessionmaker
from models import ServiceUsers

#SessionLocal = sessionmaker(autocommit=False, autoflush=False)

def get_tweets(engine):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()

    service_users = session.query(ServiceUsers).all()

    session.close()

    for service_user in service_users:
        print(f"ID: {service_user.service_user_id}, Name: {service_user.name}, MAIL: {service_user.mailaddress}")

    return {"tweets": "tweets"}
