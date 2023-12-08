from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
Base = declarative_base()

class EmpModel(Base):
    __tablename__ = "employee"
    empname = Column(String(256), primary_key=True)
    empid = Column(String(256))
    empage = Column(String(256))
    empsalaray = Column(String(256))

class EmpRegistration(BaseModel):
    employeename: str
    employeeid: str
    employeeage: str
    employeesalary: str