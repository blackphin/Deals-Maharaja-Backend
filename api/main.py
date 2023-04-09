from typing import List

from fastapi import FastAPI, Depends, Response, status, HTTPException
from fastapi.params import Body
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from sqlalchemy.orm import Session

import models
import schemas
import utils
from database import engine, get_db
from config import settings

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)
# db: Session = Depends(get_db)


@app.get("/", status_code=status.HTTP_200_OK)
def hello():
    return {"message": "Hello World"}


@app.get("/all", status_code=status.HTTP_200_OK)
def all_data(payLoad: schemas.AllAccounts, db: Session = Depends(get_db)):
    if payLoad.password == settings.database_master_password:
        if payLoad.type == "0":
            return db.query(models.Users).all()
        elif payLoad.type == "1":
            return db.query(models.Orders).all()
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@app.get("/login", status_code=status.HTTP_200_OK, response_model=schemas.AccountDetails)
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


@app.post("/create_account", status_code=status.HTTP_201_CREATED, response_model=schemas.AccountDetails)
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


@app.delete("/delete_user", status_code=status.HTTP_404_NOT_FOUND)
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


@app.get("/get_orders", status_code=status.HTTP_200_OK, response_model=List[schemas.OrderDetails])
def getOrder(payLoad: schemas.GetOrders, db: Session = Depends(get_db)):
    orders = db.query(models.Orders).filter(
        models.Orders.user_id == payLoad.user_id).all()
    if orders is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No Orders Found")
    return orders


@app.post("/create_order", status_code=status.HTTP_201_CREATED, response_model=schemas.OrderDetails)
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
