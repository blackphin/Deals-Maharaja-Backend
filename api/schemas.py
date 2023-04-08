from pydantic import BaseModel, EmailStr
from datetime import datetime


# Request Schemas

class CreateAccount(BaseModel):
    user_id: str
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    password: str


class Login(BaseModel):
    email: str
    password: str


class CreateOrder(BaseModel):
    user_id: str
    email: EmailStr
    link: str


# Response Schemas

class AccountDetails(BaseModel):
    user_id: str
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    created_at: datetime

    class Config:
        orm_mode = True


class OrderDetails(BaseModel):
    order_id: str
    user_id: str
    email: str
    link: str
    time_stamp: datetime

    class Config:
        orm_mode = True
