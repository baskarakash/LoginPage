from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from auth.jwt_handler import signJWT, decodeJWT
from fastapi.responses import JSONResponse  # Add this line
from app.models.emp_models import EmpModel, EmpRegistration
from app.models import get_db


router = APIRouter()

@router.post("/register_employee", tags=["employee"])
async def register_employee(user1: EmpRegistration, db: Session = Depends(get_db)):
    # Check if an employee with the same employeeid already exists
    existing_employee = db.query(EmpModel).filter(EmpModel.empid == user1.employeeid).first()
    if existing_employee:
        return {"message": "Employee with the same ID already exists"}

    # If the employee doesn't exist, add them to the database
    new_employee = EmpModel(
        empname=user1.employeename,
        empid=user1.employeeid,
        empage=user1.employeeage,
        empsalaray=user1.employeesalary
    )
    db.add(new_employee)
    db.commit()

    # Generate and return the access token
    access_token = signJWT(user1.employeeid)
    return {"access_token": access_token, "message": "Employee registration successful"}

@router.delete("/delete_employee/{emp_id}", tags=["employee"])
async def delete_employee_data(emp_id: str, db: Session = Depends(get_db)):
    employee = db.query(EmpModel).filter(EmpModel.empid == emp_id).first()
    if employee:
        db.delete(employee)
        db.commit()
        return {"message": "Employee data deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Employee not found")

@router.get("/get_employee/{emp_id}", response_class=JSONResponse, tags=["employee"])
async def get_employee_by_id(emp_id: str, db: Session = Depends(get_db), token: str = Depends(decodeJWT)):
    if not token:
        raise HTTPException(status_code=401, detail="Access token is missing")

    # Your additional authorization logic can go here

    employee = db.query(EmpModel).filter(EmpModel.empid == emp_id).first()

    if employee:
        employee_data = {
            "empname": employee.empname,
            "empid": employee.empid,
            "empage": employee.empage,
            "empsalaray": employee.empsalaray,
        }
        return JSONResponse(content=employee_data)
    else:
        return JSONResponse(content={"message": "Employee not present"}, status_code=404)

@router.put("/update_employee/{emp_id}", tags=["employee"])
async def update_employee_details(emp_id: str, employee_data: EmpRegistration, db: Session = Depends(get_db)):
    # Check if the employee with the specified empid exists
    existing_employee = db.query(EmpModel).filter(EmpModel.empid == emp_id).first()
    if existing_employee:
        # Update the employee's data with the provided values
        existing_employee.empname = employee_data.employeename
        existing_employee.empage = employee_data.employeeage
        existing_employee.empsalaray = employee_data.employeesalary
        db.commit()
        return {"message": "Employee details updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Employee not found")