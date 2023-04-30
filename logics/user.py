from sqlalchemy.orm import sessionmaker
from databases.service_users import ServiceUsers

SessionLocal = sessionmaker(autocommit=False, autoflush=False)

def get_service_users(engine):
    with SessionLocal(bind=engine) as session:
        service_users = session.query(ServiceUsers).all()

    return (ServiceUserModel(service_user.service_user_id, service_user.name, service_user.mailaddress) for service_user in service_users)

class ServiceUserModel:
    def __init__(self, service_user_id, name, mailaddress):
        self.service_user_id = service_user_id
        self.name = name
        self.mailaddress = mailaddress
