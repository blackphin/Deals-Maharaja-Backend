from typing import List

from fastapi import FastAPI, Depends, Response, status, HTTPException, APIRouter
from fastapi.params import Body

from pydantic import BaseModel

from sqlalchemy.orm import Session

import models
import schemas
from database import engine, get_db

router = APIRouter()


@router.post("/get_orders", status_code=status.HTTP_200_OK, response_model=List[schemas.OrderDetails])
def getOrder(payLoad: schemas.GetOrders, db: Session = Depends(get_db)):
    orders = db.query(models.Orders).filter(
        models.Orders.user_id == payLoad.user_id).all()
    if orders is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No Orders Found")
    return orders


@router.post("/create_order", status_code=status.HTTP_201_CREATED, response_model=schemas.OrderDetails)
def createOrder(payLoad: schemas.CreateOrder, db: Session = Depends(get_db)):
    if (db.query(models.Users).filter(models.Users.user_id == payLoad.user_id).first() is not None):
        new_order = models.Orders(**payLoad.dict())
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        return new_order
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User Account not Found")