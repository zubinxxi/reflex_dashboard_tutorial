from typing import Optional
import reflex as rx
from sqlmodel import Field 
from sqlalchemy.dialects import mysql

class Users(rx.Model, table=True):
    login: str = rx.Field(sa_column_args=[mysql.VARCHAR(255)])
    user_name: str = rx.Field(sa_column_args=[mysql.VARCHAR(255)])
    email: str = rx.Field(sa_column_args=[mysql.VARCHAR(255)])
    gender: str = rx.Field(sa_column_args=[mysql.VARCHAR(255)])
