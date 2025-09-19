from typing import Optional
import reflex as rx
from sqlmodel import Field, Column
from sqlalchemy.dialects import mysql

class Users(rx.Model, table=True):
    login: str = Field(sa_column=Column(mysql.VARCHAR(255)))
    user_name: str = Field(sa_column=Column(mysql.VARCHAR(255)))
    email: str = Field(sa_column=Column(mysql.VARCHAR(255)))
    gender: str = Field(sa_column=Column(mysql.VARCHAR(255)))
