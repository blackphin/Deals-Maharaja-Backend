from fastapi import FastAPI, Depends, Response, status, HTTPException
from fastapi.params import Body

from pydantic import BaseModel

from sqlalchemy.orm import Session

import models
import schemas
import utils
from database import engine, get_db


app = FastAPI()
models.Base.metadata.create_all(bind=engine)
# db: Session = Depends(get_db)


@app.get("/", status_code=status.HTTP_200_OK)
def hello():
    return {"message": "Hello World"}


@app.get("/login", status_code=status.HTTP_200_OK, response_model=schemas.AccountDetails)
def login(payLoad: schemas.Login, db: Session = Depends(get_db)):
    user_data = db.query(models.Users).filter(
        models.Users.email == payLoad.email).first()

    if user_data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Account Doesn't Exist")

    elif (payLoad.email == user_data.email and utils.verify(payLoad.password, user_data.password) == True):
        # Set user as active
        return user_data

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid Credentials")


@app.post("/create_account", status_code=status.HTTP_201_CREATED, response_model=schemas.AccountDetails)
def createAccount(payLoad: schemas.CreateAccount, db: Session = Depends(get_db)):
    user_query = db.query(models.Users).filter(
        models.Users.user_id == payLoad.user_id)
    # if (payLoad.user_id == user_query.first().user_id):
    #     raise HTTPException(status_code=status.HTTP_409_CONFLICT,
    #                         detail="Account Already Exists")
    # else:
    payLoad.password = utils.hash(payLoad.password)
    new_user = models.Users(**payLoad.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post("/create_order", status_code=status.HTTP_201_CREATED, response_model=schemas.OrderDetails)
def createOrder(payLoad: schemas.CreateOrder, db: Session = Depends(get_db)):
    new_order = models.Orders(**payLoad.dict())
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order
