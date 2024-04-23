from pydantic import BaseModel
from typing import List, Mapping
from datetime import datetime


class Product(BaseModel):
    name: str
    price: float
