from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
import database
from models import User
from pydantic import BaseModel
import models
from passlib.context import CryptContext


router = APIRouter(
    tags=['Users']
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserBase(BaseModel):
    name:str
    email:str
    password: str

def get_password(password:str):
    return pwd_context.hash(password)



@router.post('/user', response_model=UserBase)
def create_user(request: UserBase, db: Session = Depends(database.get_db)):
    user_exist=db.query(models.User).filter(models.User.email == request.email).first()
    if user_exist:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail="Record already exist.")
    hashed_password=get_password(request.password)
    
    new_user = models.User(
        name=request.name,
        email=request.email,
        password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return UserBase(name=new_user.name,email= new_user.email,password=new_user.password)
    


@router.get('/user/{id}')
def get_user(id: int,request: UserBase, db: Session = Depends(database.get_db)):
    return User.show(id, db)



