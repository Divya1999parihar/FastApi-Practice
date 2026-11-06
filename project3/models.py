
from pydantic import BaseModel, Field
from typing import Optional

class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    quantity: int

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(default=None, ge=0.0)
    quantity: Optional[int] = Field(default=None, ge=0)

class ProductCreate(BaseModel):
    id: Optional[int] = None
    name: str
    description: str
    price: float
    quantity: int


#def _init_(self, id:int, name:str, description:str, price:float, quantity:int):
 #   self.id= id
 #  self.name= name
 #   self.description= description  (this is a constructor)
 #   self.price= price
 #   self.quantity = quantity
    