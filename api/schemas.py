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
    email: EmailStr
    password: str


# Addresses


class GetAddress(BaseModel):
    user_id: str
    email: EmailStr


class DelAddress(BaseModel):
    user_id: str
    email: EmailStr
    address_id: str


class AddAddress(BaseModel):
    user_id: str
    email: EmailStr
    address: str
    city: str
    state: str
    pincode: str


class UpdateAddress(BaseModel):
    user_id: str
    address_id: str
    email: EmailStr
    address: str
    city: str
    state: str
    pincode: str


# Points


class GetPoints(BaseModel):
    user_id: str
    email: EmailStr


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
    email: EmailStr


class VerifyOrder(BaseModel):
    user_id: str
    email: EmailStr
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


# Points

class PointsTransactionDetails(BaseModel):
    time_stamp: datetime
    user_id: str
    email: EmailStr
    transaction_id: str
    type: str
    points: str
    balance: str

    class Config:
        orm_mode = True


# Activity


class ActivityDetails(BaseModel):
    activity_id: str
    user_id: str
    email: EmailStr
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
    email: EmailStr
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
