from typing import List

from fastapi import FastAPI, Depends, Response, status, HTTPException, APIRouter
from fastapi.params import Body

from pydantic import BaseModel

from sqlalchemy.orm import Session

import models
import schemas
from database import engine, get_db

router = APIRouter(
    prefix="/address",
)


@router.post("/get", status_code=status.HTTP_200_OK, response_model=List[schemas.AddressDetails])
def getAddresses(payLoad: schemas.GetOrders, db: Session = Depends(get_db)):
    addresses = db.query(models.Addresses).filter(
        models.Addresses.user_id == payLoad.user_id).all()
    if addresses is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No Addresses Found")
    return addresses


@router.post("/add", status_code=status.HTTP_201_CREATED, response_model=schemas.AddressDetails)
def addAddress(payLoad: schemas.AddAddress, db: Session = Depends(get_db)):
    if (db.query(models.Users).filter(models.Users.user_id == payLoad.user_id).first() is not None):
        new_address = models.Addresses(**payLoad.dict())
        db.add(new_address)
        db.commit()
        db.refresh(new_address)
        return new_address
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User Account not Found")


@router.delete("/delete", status_code=status.HTTP_404_NOT_FOUND)
def deleteAddress(payLoad: schemas.DelAddress, db: Session = Depends(get_db)):
    user_data = db.query(models.Users).filter(
        models.Users.user_id == payLoad.user_id)

    address_data = db.query(models.Addresses).filter(
        models.Addresses.address_id == payLoad.address_id)

    print(payLoad.address_id)

    if user_data.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Account Doesn't Exist")

    elif (payLoad.address_id == address_data.first().address_id and payLoad.user_id == address_data.first().user_id):
        address_data.delete(synchronize_session=False)
        db.commit()
        return {"message": "Address Deleted"}

    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Address Doesn't Exist")
