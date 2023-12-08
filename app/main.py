from fastapi import FastAPI, Header, Depends, HTTPException, APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.models import get_db
from app.models.emp_models import EmpRegistration
from auth.jwt_handler import decodeJWT, signJWT

app = FastAPI()
router = APIRouter()

MIN_TOKEN_LENGTH = 50

async def get_current_user(token: str = Depends(decodeJWT)):
    if not token:
        raise HTTPException(status_code=401, detail="Invalid token")
    return token

@router.post("/submitted", tags=["user"], response_model=dict)
async def login_user(
    user_data: EmpRegistration,
    authorization: str = Header(...),  # Require the Authorization header
    db: Session = Depends(get_db),
):
    # Check if the Authorization header is in the correct format
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format in Authorization header")

    # Extract the token value
    token_value = authorization[len("Bearer "):].strip()

    # Validate the token length
    if len(token_value) < MIN_TOKEN_LENGTH:
        raise HTTPException(status_code=401, detail="Invalid token length")

    try:
        # Validate the token
        current_user = get_current_user(token_value)

        # If the token is valid, return a message
        return {"message": "Successful Login!!!"}
    except HTTPException as e:
        # If there is an exception, handle it
        if e.status_code == 401:
            # If it's a 401 status code, return a message indicating no access
            raise HTTPException(status_code=401, detail="No access to login")
        else:
            # Otherwise, re-raise the exception
            raise

@router.post("/register", tags=["user"], response_model=dict)
async def register_user(
    user_data: EmpRegistration,
    db: Session = Depends(get_db),
):
    # Your implementation for user registration goes here
    pass

@router.post("/register_employee", tags=["employee"])
async def register_employee(
    user1: EmpRegistration,
    db: Session = Depends(get_db)
):
    # Your existing implementation for employee registration goes here
    pass

@router.delete("/delete_employee/{emp_id}", tags=["employee"])
async def delete_employee_data(emp_id: str, db: Session = Depends(get_db)):
    # Your existing implementation for deleting employee data goes here
    pass

@router.get("/get_employee/{emp_id}", response_class=JSONResponse, tags=["employee"])
async def get_employee_by_id(emp_id: str, db: Session = Depends(get_db)):
    # Your existing implementation for getting employee data goes here
    pass

@router.put("/update_employee/{emp_id}", tags=["employee"])
async def update_employee_details(emp_id: str, employee_data: EmpRegistration, db: Session = Depends(get_db)):
    # Your existing implementation for updating employee details goes here
    pass

# Include this router in the main FastAPI application
app.include_router(router)
