from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from sqlalchemy import Column, Integer, String, LargeBinary
from sqlalchemy.orm import Session
from database import Base, get_db
import models
import os
from uuid import uuid4


router = APIRouter(
    tags=["Uploads"]
)

@router.post("/create_file")
async def create_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_content = await file.read()
    db_file = models.uploadedFile(
        filename=file.filename,
        content_type=file.content_type,
        data=file_content
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    
    return {
        "id": db_file.id, "filename": db_file.filename,"content_type": db_file.content_type
    }



@router.get("/get_file/{name}")
async def get_file(name: str, db: Session = Depends(get_db)):
    db_file = db.query(models.uploadedFile).filter(models.uploadedFile.filename == name).first()
    if db_file is None:
        raise HTTPException (status_code=404, detail="File not found")
    else:
        return {
                "filename": db_file.filename, "content_type": db_file.content_type, "data": db_file.data
    }


# Storing file in local storage


@router.post("/local_file")
async def local_file(file: UploadFile = File(...)):

# first we have to create a folder 
    Create_folder="./upload_files"
    if not os.path.exists(Create_folder):
        os.mkdir(Create_folder)
    else:
# to generate unique name we use uuid4
        unique_name=f"{uuid4()}_{file.filename}"
# to save the file we use the path library
    file_path = os.path.join(Create_folder, unique_name)
    with open(file_path, "wb") as f:
        f.write(await file.read())
        return {"filename": file.filename, "content_type": file.content_type}



        






