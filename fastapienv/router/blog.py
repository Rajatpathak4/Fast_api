from fastapi import APIRouter, Depends, HTTPException, FastAPI
from typing import List
from sqlalchemy.orm import Session
from pydantic import BaseModel
import models
import database
from passlib.context import CryptContext
 
router=APIRouter(
    tags=["Blogs"]
)

class BlogBase(BaseModel):
    title: str
    body: str
    password: str


pwd_context=CryptContext(schemes=["bcrypt"], deprecated= "auto")

def get_password(password:str):
    print(password)
    return pwd_context.hash(password)



@router.post("/blogs", tags=["Blogs"])
def create_user(request: BlogBase ,db: Session= Depends(database.get_db)):
    hash_password=get_password(request.password)
    print(hash_password)
    new_base=models.Blog(
        title=request.title ,
        body=request.body,
        password=hash_password
        )
    db.add(new_base)
    db.commit()
    db.refresh(new_base)
    return new_base




@router.get("/blogs/{id}")
def get_user(id: int, db:Session= Depends(database.get_db)):
    get_user=db.query(models.Blog).filter(models.Blog.id == id).first()
    if not get_user:
        raise HTTPException(status_code=404 , detail="Blog not Found")
    return get_user


# @router.get("/blogs")
# def get_all(db:Session= Depends(database.get_db)):
#     return db.query(models.Blog).all()



@router.delete("/blogs/{id}/")
def delete_user(id : int, db:Session=Depends(database.get_db)):
    delete=db.query(models.Blog).filter(models.Blog.id==id).first()
    db.delete(delete)
    db.commit()
    return {"message": "Blog deleted successfully"}



@router.put("/blogs/{id}")
def update_blog(id: int, request: BlogBase, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    blog.title = request.title
    blog.body = request.body
    # hash_password=0
    # blog.password = hash_password(request.password)  
    db.commit()
    db.refresh(blog)
    return blog
