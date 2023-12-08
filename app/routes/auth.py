# app/routes/auth.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_database
from auth.jwt_handler import signJWT
from app.models.auth_models import AuthModel
from app.models.user_models import UserRegistration

router = APIRouter()

@router.post("/register", tags=["auth"], response_model=dict)
async def register_user(
    user_data: UserRegistration,
    db: Session = Depends(get_database)
):
    existing_user = db.query(AuthModel).filter(AuthModel.userid == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    if user_data.password != user_data.repeat_password:
        raise HTTPException(status_code=400, detail="Password and Repeat password do not match")

    new_user = AuthModel(userid=user_data.username, pas=user_data.password)
    db.add(new_user)
    db.commit()

    access_token = signJWT(new_user.userid)

    return {"message": "Registration successful", "access_token": access_token}
