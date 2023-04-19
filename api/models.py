from sqlalchemy import Column, Boolean, Integer, String
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from database import Base


class Users(Base):
    __tablename__ = "users"

    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    user_id = Column(Integer, primary_key=True, nullable=False)
    is_active = Column(Boolean, server_default='False', nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    points = Column(Integer, nullable=False, server_default=text('0'))


class Activity(Base):
    __tablename__ = "activity"

    time_stamp = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    activity_id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    email = Column(String, nullable=False)
    link = Column(String, nullable=False)


class Orders(Base):
    __tablename__ = "orders"

    time_stamp = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    user_id = Column(Integer, nullable=False)
    email = Column(String, nullable=False)
    advertiser = Column(String, nullable=False)
    order_id = Column(String, primary_key=True, nullable=False)
    order_value = Column(Integer, nullable=False)
    commision = Column(Integer, nullable=False)


class Addresses(Base):
    __tablename__ = "addresses"

    address_id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    pincode = Column(String, nullable=False)
