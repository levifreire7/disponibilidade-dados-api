from decimal import Decimal
from pydantic import BaseModel

class Message(BaseModel):
    message: str

class TotalAmount(BaseModel):
    total: Decimal