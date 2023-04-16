from typing import List

from fastapi import FastAPI, Depends, Response, status, HTTPException, APIRouter
from fastapi.params import Body
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from sqlalchemy.orm import Session

import models
import schemas
import utils
from database import engine, get_db

router = APIRouter()

@router.post("/login", status_code=status.HTTP_200_OK, response_model=schemas.AccountDetails)
def login(payLoad: schemas.Login, db: Session = Depends(get_db)):
    user_data = db.query(models.Users).filter(
        models.Users.email == payLoad.email)

    if user_data.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Account Doesn't Exist")

    elif (payLoad.email == user_data.first().email and utils.verify(payLoad.password, user_data.first().password) == True):
        # SET USER AS ACTIVE
        return user_data.first()

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid Credentials")


@router.post("/create_account", status_code=status.HTTP_201_CREATED, response_model=schemas.AccountDetails)
def createAccount(payLoad: schemas.CreateAccount, db: Session = Depends(get_db)):
    user_query = db.query(models.Users).filter(
        models.Users.phone == payLoad.phone)
    if user_query.first() is None:
        payLoad.password = utils.hash(payLoad.password)
        new_user = models.Users(**payLoad.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Account Already Exists")


@router.delete("/delete_user", status_code=status.HTTP_404_NOT_FOUND)
def deleteUser(payLoad: schemas.Login, db: Session = Depends(get_db)):
    user_data = db.query(models.Users).filter(
        models.Users.email == payLoad.email)

    if user_data.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Account Doesn't Exist")

    elif (payLoad.email == user_data.first().email and utils.verify(payLoad.password, user_data.first().password) == True):
        # SET USER AS ACTIVE
        user_data.delete(synchronize_session=False)
        db.commit()
        return {"message": "Account Deleted"}

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid Credentials")