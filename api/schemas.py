from pydantic import BaseModel, EmailStr
from datetime import datetime


# Request Schemas


class AllAccounts(BaseModel):
    type: str
    password: str

# Users


class CreateAccount(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    password: str


class Login(BaseModel):
    email: str
    password: str


# Addresses


class GetAddress(BaseModel):
    user_id: str
    email: str


class DelAddress(BaseModel):
    user_id: str
    email: str
    address_id: str


class AddAddress(BaseModel):
    user_id: str
    email: str
    address: str
    city: str
    state: str
    pincode: str


class UpdateAddress(BaseModel):
    user_id: str
    address_id: str
    email: str
    address: str
    city: str
    state: str
    pincode: str


# Activity


class AddActivity(BaseModel):
    user_id: str
    email: EmailStr
    link: str


class GetActivity(BaseModel):
    user_id: str
    email: EmailStr


# Orders

class CreateOrder(BaseModel):
    user_id: str
    email: EmailStr
    order_id: str
    advertiser: str
    order_value: str
    commision: str


class GetOrders(BaseModel):
    user_id: str
    email: str


class VerifyOrder(BaseModel):
    user_id: str
    email: str
    order_id: str


# Response Schemas


# Users


class AccountDetails(BaseModel):
    user_id: str
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    created_at: datetime

    class Config:
        orm_mode = True


# Addresses


class AddressDetails(BaseModel):
    address_id: str
    user_id: str
    address: str
    city: str
    state: str
    pincode: str

    class Config:
        orm_mode = True


# Activity


class ActivityDetails(BaseModel):
    activity_id: str
    user_id: str
    email: str
    link: str
    time_stamp: datetime

    class Config:
        orm_mode = True


# Orders


class OrderDetails(BaseModel):
    time_stamp: datetime
    order_id: str
    order_value: str
    commision: str
    user_id: str
    email: str
    advertiser: str

    class Config:
        orm_mode = True


class OrderVerified(BaseModel):
    order_id: str
    order_value: str
    commision: str
    advertiser: str

    class Config:
        orm_mode = True
