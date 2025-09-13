from typing import Optional
import reflex as rx
from sqlmodel import Field 

class Users(rx.Model, table=True):
    login: str
    user_name: str
    email: str
    gender: str
