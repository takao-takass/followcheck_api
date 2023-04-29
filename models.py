from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class ServiceUsers(Base):
    __tablename__ = "service_users"

    service_user_id = Column(String(255), primary_key=True)
    name = Column(String(255))
    mailaddress = Column(String(255))
    password = Column(String(255))
    deleted = Column(Integer)
