from pydantic import BaseModel
from typing import List, Mapping
from datetime import datetime


class Cart(BaseModel):
    user_id: int
    products: list[str]
