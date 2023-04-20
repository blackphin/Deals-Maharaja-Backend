from typing import List
from datetime import datetime, date
from dateutil import parser
import requests
import json

from fastapi import FastAPI, Depends, Response, status, HTTPException, APIRouter
from fastapi.params import Body

from pydantic import BaseModel

from sqlalchemy.orm import Session

import models
import schemas
from database import engine, get_db
from config import settings

router = APIRouter(
    prefix="/orders"
)


@router.post("/get", status_code=status.HTTP_200_OK, response_model=List[schemas.OrderDetails])
def getOrders(payLoad: schemas.GetOrders, db: Session = Depends(get_db)):
    orders_data = db.query(models.Orders).filter(
        models.Orders.user_id == payLoad.user_id)
    user_data = db.query(models.Users).filter(
        models.Users.user_id == payLoad.user_id)
    if (orders_data.all() is None or user_data.first() is None):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No Orders Found")
    elif (user_data.first().email == payLoad.email):
        return orders_data.all()


@router.post("/add", status_code=status.HTTP_201_CREATED, response_model=schemas.OrderDetails)
def addOrder(payLoad: schemas.CreateOrder, db: Session = Depends(get_db)):
    user_data = db.query(models.Users).filter(
        models.Users.user_id == payLoad.user_id)
    if (user_data.first() is not None and user_data.first().email == payLoad.email):
        new_order = models.Orders(**payLoad.dict())
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        user_data.update({"points": str(new_order.commision)},
                         synchronize_session=False)
        db.commit()
        return new_order
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User Account not Found")


@router.post("/verify", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.OrderVerified)
def verifyOrder(payLoad: schemas.VerifyOrder, db: Session = Depends(get_db)):
    now = datetime.now().strftime("%Y-%m-%d")
    user_data = db.query(models.Users).filter(
        models.Users.user_id == payLoad.user_id)
    activity_data = db.query(models.Activity).filter(
        models.Activity.user_id == payLoad.user_id)

    if (user_data.first() is None or activity_data.first() is None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User Account not Found")
    elif (user_data.first().email == payLoad.email):
        url = f"https://public.api.optimisemedia.com/v1/conversions?agencyId=95&contactId={settings.optimisemedia_contact_id}&fromDate=2023-04-01&toDate={now}&dateField=conversion"
        headers = {
            'apikey': settings.optimisemedia_api_key
        }
        response = requests.request("GET", url, headers=headers, data="")
        converted_orders = json.loads(response.text)
        for converted_order in converted_orders:
            # conversion_time = parser.parse(
            #     converted_order["conversionDate"]).astimezone().strftime("%m/%d/%Y, %H:%M:%S")
            # click_time = parser.parse(
            #     converted_order["clickDate"]).astimezone().strftime("%m/%d/%Y, %H:%M:%S")
            # backend_click_time = activity_data.order_by(
            #     models.Activity.activity_id.desc()).first().time_stamp.strftime("%m/%d/%Y, %H:%M:%S")
            order_id = converted_order["advertiserRef"]
            if (order_id == payLoad.order_id):
                order_value = int(converted_order["conversionValue"]["amount"])
                commision = int(converted_order["commission"]["amount"])
                advertiser = converted_order["advertiserName"]
                return {"order_id": order_id, "order_value": order_value, "commision": commision, "advertiser": advertiser}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="No Account Found")
