from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class AuthModel(Base):
    __tablename__ = "auth"
    userid = Column(String(256), primary_key=True)
    pas = Column(String(256))