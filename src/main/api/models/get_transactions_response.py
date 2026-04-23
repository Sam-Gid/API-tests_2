from datetime import datetime
from typing import Optional
from src.main.api.models.base_model import BaseModel


class Transactions(BaseModel):
    transactionId: int
    type: str
    amount: float
    fromAccountId: Optional[int]
    toAccountId: Optional[int]
    createdAt: datetime
    creditId: Optional[int]

class GetTransactionsResponse(BaseModel):
    id: int
    number: str
    balance: float
    transactions: list[Transactions]