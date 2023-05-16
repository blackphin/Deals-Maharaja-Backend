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

commision_percentage = 65/100


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


@router.post("/verify", status_code=status.HTTP_201_CREATED, response_model=schemas.OrderVerified)
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
        try:
            url = f"https://public.api.optimisemedia.com/v1/conversions?agencyId=95&contactId={settings.optimisemedia_contact_id}&fromDate=2023-04-01&toDate={now}&dateField=conversion"
            headers = {
                'apikey': settings.optimisemedia_api_key
            }
            response = requests.request("GET", url, headers=headers, data="")
            converted_orders = json.loads(response.text)
            flag = False
            for converted_order in converted_orders:
                # conversion_time = parser.parse(
                #     converted_order["conversionDate"]).astimezone().strftime("%m/%d/%Y, %H:%M:%S")
                # click_time = parser.parse(
                #     converted_order["clickDate"]).astimezone().strftime("%m/%d/%Y, %H:%M:%S")
                # backend_click_time = activity_data.order_by(
                #     models.Activity.activity_id.desc()).first().time_stamp.strftime("%m/%d/%Y, %H:%M:%S")
                order_id = converted_order["advertiserRef"]
                if (order_id == payLoad.order_id):

                    order_value = int(
                        converted_order["conversionValue"]["amount"])
                    commision = int(
                        converted_order["commission"]["amount"])
                    advertiser = converted_order["advertiserName"]
                    new_order_dict = {"user_id": payLoad.user_id, "email": payLoad.email, "order_id": order_id,
                                      "order_value": order_value, "commision": commision, "advertiser": advertiser}
                    new_order = models.Orders(**new_order_dict)
                    db.add(new_order)
                    db.commit()
                    db.refresh(new_order)

                    points = user_data.first().points + new_order.commision

                    user_data.update({"points": points},
                                     synchronize_session=False)
                    transaction_data_dict = {"user_id": payLoad.user_id, "email": payLoad.email, "points": int(
                        new_order.commision)*commision_percentage, "type": "cr", "balance": points}
                    db.add(models.PointsTransaction(**transaction_data_dict))
                    db.commit()
                    flag = True

                    return new_order

            if (flag == False):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="Order Not Found")
        except:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                                detail="Error in Optimise Media API")
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="No Account Found")
