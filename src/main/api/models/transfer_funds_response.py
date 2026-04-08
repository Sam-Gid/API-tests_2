from src.main.api.models.base_model import BaseModel


class TransferFundsResponse(BaseModel):
    fromAccountId: int
    toAccountId: int
    fromAccountIdBalance: float