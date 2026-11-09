
from pydantic import BaseModel, Field
from typing import Optional

class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    quantity: int

class ProductUpdate(BaseModel):
    name: str = Field(default=None)
    description: Optional[str] = None
    price: float = Field(default=None, ge=0)
    quantity: Optional[int] = Field(default=1, ge=0)

class ProductCreate(BaseModel):
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
    