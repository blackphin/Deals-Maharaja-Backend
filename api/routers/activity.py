from typing import List

from fastapi import FastAPI, Depends, Response, status, HTTPException, APIRouter
from fastapi.params import Body

from pydantic import BaseModel

from sqlalchemy.orm import Session

import models
import schemas
from database import engine, get_db

router = APIRouter(
    prefix="/activity"
)


@router.post("/get", status_code=status.HTTP_200_OK, response_model=List[schemas.ActivityDetails])
def getActivity(payLoad: schemas.GetActivity, db: Session = Depends(get_db)):
    user_data = db.query(models.Users).filter(
        models.Users.user_id == payLoad.user_id).first()
    if user_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="No Account Found")
    elif (user_data.email == payLoad.email):
        activity = db.query(models.Activity).filter(
            models.Activity.user_id == payLoad.user_id).all()
        return activity
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="No Account Found")


@router.post("/add", status_code=status.HTTP_201_CREATED, response_model=schemas.ActivityDetails)
def addActivity(payLoad: schemas.AddActivity, db: Session = Depends(get_db)):
    user_data = db.query(models.Users).filter(
        models.Users.user_id == payLoad.user_id).first()
    if (user_data is None):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No Account Found"
        )
    elif (user_data.email == payLoad.email):
        new_activity = models.Activity(**payLoad.dict())
        db.add(new_activity)
        db.commit()
        db.refresh(new_activity)
        return new_activity
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="No Account Found")
