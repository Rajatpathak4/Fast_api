from datetime import datetime, timedelta
from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
import models

SECRET_KEY = "cb2e76edb31427f002df8973228a2fc0dc1ec4a3aaf9d00d3a332bcb0d102bb0"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter(tags=["JWT_authentication"])


class Token(BaseModel):
    access_token: str
    token_type: str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_hashed_password(password: str):
    return pwd_context.hash(password)



def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "sub": data.get("name")})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    return payload




def get_user(name: str, db: Session=Depends(get_db)):
    return db.query(models.JWTuser).filter(models.JWTuser.name == name).first()



def authenticate_user(name: str, password: str, db: Session= Depends(get_db)):
    user = db.query(models.JWTuser).filter(models.JWTuser.name == name).first()
    if not user or not verify_password(password, user.password):
        return None
    return user




@router.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    access_token = create_access_token(data={"name": user.name})
    return {"access_token": access_token, "token_type": "bearer"}



@router.get("/users")
def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    name = decode_token(token)
    user = get_user(name, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid user")
    return {"name": user.name, "email": user.email}


class CreateUser(BaseModel):
    name:str
    email: str
    password: str

@router.post("/create_user")
def create_user(createUser:CreateUser, db: Session = Depends(get_db)):
    hashed_password = get_hashed_password(createUser.password)
    new_user = models.JWTuser(name=createUser.name, email=createUser.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg": "User created successfully"}
