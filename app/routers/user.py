from .. import models, schemas, utils
from fastapi import FastAPI, HTTPException, status, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import engine, get_db
from typing import Optional, List

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.UserOut)
def create_user(user: schemas.UserCreate,db:Session =  Depends(get_db)):
    
    #hash password-user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    
    user_data = user.model_dump(exclude_unset=True)
    new_user = models.User(**user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db : Session = Depends(get_db)):
   user = db.query(models.User).filter(models.User.id == user_id).first()
   if not user:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"User with id: {user_id} is not found!")
    
   return user