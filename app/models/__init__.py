from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

DATABASE_URL = "postgresql://postgres:root@localhost:5432/login"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

def create_tables():
    # Import models and create tables
    from . import auth_models, emp_models, user_models
    Base.metadata.create_all(bind=engine)
