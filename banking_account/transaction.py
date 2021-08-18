from typing import Optional
from pydantic import BaseModel

class Transaction(BaseModel):
    type: str
    origin: Optional[str] = None
    destination: Optional[str] = None
    amount: int

class Account_balance(BaseModel):
    id: str
    balance: int

class Transaction_response(BaseModel):
    origin: Optional[Account_balance] = None
    destination: Optional[Account_balance] = None
