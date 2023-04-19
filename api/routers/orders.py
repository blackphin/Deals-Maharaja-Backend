from typing import List
from datetime import datetime
import requests
import json

from fastapi import FastAPI, Depends, Response, status, HTTPException, APIRouter
from fastapi.params import Body

from pydantic import BaseModel

from sqlalchemy.orm import Session

import models
import schemas
from database import engine, get_db

router = APIRouter(
    prefix="/orders"
)


@router.post("/get", status_code=status.HTTP_200_OK, response_model=List[schemas.OrderDetails])
def getOrders(payLoad: schemas.GetOrders, db: Session = Depends(get_db)):
    orders = db.query(models.Orders).filter(
        models.Orders.user_id == payLoad.user_id).all()
    if orders is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No Orders Found")
    # remove fromm here
    print(orders[0].time_stamp.strftime("%m/%d/%Y, %H:%M:%S"))

    url = "https://public.api.optimisemedia.com/v1/conversions?agencyId=95&contactId=2340252&fromDate=2023-04-01&toDate=2023-04-18&dateField=conversion"

    payload = ""
    headers = {
        'apikey': '5ydj62ESZqHKckZMZwmbgef0hKSFAr7MSf9vnIEJk9Q='
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    list1 = json.loads(response.text)
    print((list1[0]["conversionDate"]))
    # till here
    return orders


@router.post("/add", status_code=status.HTTP_201_CREATED, response_model=schemas.OrderDetails)
def addOrder(payLoad: schemas.CreateOrder, db: Session = Depends(get_db)):
    if (db.query(models.Users).filter(models.Users.user_id == payLoad.user_id).first() is not None):
        new_order = models.Orders(**payLoad.dict())
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        return new_order
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User Account not Found")


# @router.post("/verify_order", status_code=status.HTTP_202_ACCEPTED)
# def verifyOrder(payLoad: schemas.VerifyOrder, db: Session = Depends(get_db)):
#     return 0
