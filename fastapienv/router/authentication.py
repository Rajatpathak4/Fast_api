from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
import models
import database
import token
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from pydantic import BaseModel


router = APIRouter(tags=['Authentication'])

pwd_context=CryptContext(schemes=["bcrypt"], deprecated= "auto")

class login(BaseModel):
    username: str
    password: str



class Hash():
    def get_password(password:str):
        return pwd_context.hash(password)



@router.post('/login')
def login(request: login ,db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    return user
    
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect password")

    access_token = token.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}