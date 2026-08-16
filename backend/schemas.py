from pydantic import BaseModel
from datetime import date
from typing import Optional


class ProductResponse(BaseModel):
    id: int
    product_name: str
    category: Optional[str] = None
    sub_category: Optional[str] = None

    class Config:
        from_attributes = True


class SaleResponse(BaseModel):
    id: int
    product_id: int
    sale_date: date
    quantity: int
    sales_amount: Optional[float] = None
    profit: Optional[float] = None

    class Config:
        from_attributes = True


class InventoryResponse(BaseModel):
    id: int
    product_id: int
    current_stock: int
    reorder_level: Optional[int] = None
    safety_stock: Optional[int] = None

    class Config:
        from_attributes = True


class ForecastResponse(BaseModel):
    product_id: int
    forecast_date: date
    predicted_quantity: float
    model_name: Optional[str] = None

    class Config:
        from_attributes = True

from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    role: str
    user_id: int
    name: str