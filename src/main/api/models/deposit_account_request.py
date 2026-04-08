from src.main.api.models.base_model import BaseModel


class DepositAccount(BaseModel):
    accountId: int
    amount: int