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
def getAddresses(payLoad: schemas.GetAddress, db: Session = Depends(get_db)):
    addresses = db.query(models.Addresses).filter(
        models.Addresses.user_id == payLoad.user_id).all()
    user_data = db.query(models.Users).filter(
        models.Users.user_id == payLoad.user_id)
    if addresses is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No Addresses Found")
    elif (user_data.first() is not None and user_data.first().email == payLoad.email):
        return addresses
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="No Account Found")


@router.post("/add", status_code=status.HTTP_201_CREATED, response_model=schemas.AddressDetails)
def addAddress(payLoad: schemas.AddAddress, db: Session = Depends(get_db)):
    user_data = db.query(models.Users).filter(
        models.Users.user_id == payLoad.user_id)
    if (user_data.first() is not None and user_data.first().email == payLoad.email):
        new_address = models.Addresses(user_id=payLoad.user_id, address=payLoad.address,
                                       city=payLoad.city, state=payLoad.city, pincode=payLoad.city)
        db.add(new_address)
        db.commit()
        db.refresh(new_address)
        return new_address
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User Account not Found")


@router.put("/update", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.AddressDetails)
def updateAddress(payLoad: schemas.UpdateAddress, db: Session = Depends(get_db)):
    address_data = db.query(models.Addresses).filter(
        models.Addresses.address_id == payLoad.address_id)

    user_data = db.query(models.Users).filter(
        models.Users.user_id == payLoad.user_id)

    if address_data.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Address Doesn't Exist")

    elif (user_data.first().email != payLoad.email):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Email Doesn't Match")

    elif (payLoad.address_id == str(address_data.first().address_id) and payLoad.user_id == str(address_data.first().user_id)):
        payload_dict = payLoad.dict()
        payload_dict.pop("email")
        address_data.update(payload_dict, synchronize_session=False)
        db.commit()
        return address_data.first()

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="No Account Found")


@router.delete("/delete", status_code=status.HTTP_404_NOT_FOUND)
def deleteAddress(payLoad: schemas.DelAddress, db: Session = Depends(get_db)):
    user_data = db.query(models.Users).filter(
        models.Users.user_id == payLoad.user_id)

    address_data = db.query(models.Addresses).filter(
        models.Addresses.address_id == payLoad.address_id)

    if user_data.first() is None or address_data.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Account Doesn't Exist")

    elif (user_data.first().email != payLoad.email):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Email Doesn't Match")

    elif (payLoad.address_id == str(address_data.first().address_id) and payLoad.user_id == str(address_data.first().user_id)):
        address_data.delete(synchronize_session=False)
        db.commit()
        return {"message": "Address Deleted"}

    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Address Doesn't Exist")
