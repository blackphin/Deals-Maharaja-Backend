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


class Orders(Base):
    __tablename__ = "orders"

    time_stamp = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    order_id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    email = Column(String, nullable=False)
    link = Column(String, nullable=False)