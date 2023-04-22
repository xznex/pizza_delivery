from pydantic import BaseModel
from typing import Optional


class SignUpModel(BaseModel):
    id: Optional[int]
    username: str
    email: str
    password: str
    is_staff: Optional[bool]
    is_active: Optional[bool]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "username": "john",
                "email": "john@gmail.com",
                "password": "password",
                "is_staff": False,
                "is_active": True
            }
        }


class Settings(BaseModel):
    authjwt_secret_key: str = "ecbbf13aea4aa9feb22f9da201294aec021acb197251be1651055ed92ae77299"


class LoginModel(BaseModel):
    username: str
    password: str


class OrderModel(BaseModel):
    id: Optional[int]
    quantity: int
    order_status: Optional[str] = "PENDING"
    pizza_size: Optional[str] = "MEDIUM"
    flavour: Optional[str]
    user_id: Optional[int]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "quantity": 2,
                "pizza_size": "LARGE",
                "flavour": "pepperoni",
            }
        }


class OrderStatusModel(BaseModel):
    order_status: Optional[str] = "PENDING"

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "order_status": "IN-TRANSIT"
            }
        }
