from sqlalchemy.orm import sessionmaker
from databases.service_users import ServiceUsers

def get_service_users(engine):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    session = SessionLocal()

    service_users = session.query(ServiceUsers).all()

    session.close()

    service_users = [ServiceUserModel(service_user.service_user_id, service_user.name, service_user.mailaddress) for service_user in service_users]

    return service_users

class ServiceUserModel:
    def __init__(self, service_user_id, name, mailaddress):
        self.service_user_id = service_user_id
        self.name = name
        self.mailaddress = mailaddress


