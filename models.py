from pydantic import BaseModel, Field
from typing import Optional

class ProductCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=80)
    price: int = Field(..., ge=0)
    in_stock: bool = True

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=80)
    price: Optional[int] = Field(None, ge=0)
    in_stock: Optional[bool] = None

class ProductOut(BaseModel):
    id: int
    name: str
    price: int
    in_stock: bool
