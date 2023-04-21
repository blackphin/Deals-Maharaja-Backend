from typing import List

from fastapi import FastAPI, Depends, Response, status, HTTPException, APIRouter
from fastapi.params import Body

from pydantic import BaseModel

from sqlalchemy.orm import Session

import models
import schemas
from database import engine, get_db

router = APIRouter(
    prefix="/points"
)


@router.post("/get", status_code=status.HTTP_200_OK, response_model=List[schemas.PointsTransactionDetails])
def getActivity(payLoad: schemas.GetPoints, db: Session = Depends(get_db)):
    user_data = db.query(models.Users).filter(
        models.Users.user_id == payLoad.user_id).first()
    if user_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="No Account Found")
    elif (user_data.email == payLoad.email):
        transaction_details = db.query(models.Points).filter(
            models.Activity.user_id == payLoad.user_id).all()
        return transaction_details
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="No Account Found")
