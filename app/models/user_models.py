from pydantic import BaseModel, Field

class EmpRegistration(BaseModel):
    employeename: str
    employeeid: str
    employeeage: str
    employeesalary: str

class UserRegistration(BaseModel):
    username: str
    password: str
    repeat_password: str

class UserSchema(BaseModel):
    name: str = Field(default=None)
    password: str = Field(default=None)

class UserLoginSchema(BaseModel):
    name: str = Field(default=None)
    password: str = Field(default=None)

class UserLoginJSON(BaseModel):
    username: str
    password: str