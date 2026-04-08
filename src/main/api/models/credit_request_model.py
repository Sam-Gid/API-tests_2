from src.main.api.models.base_model import BaseModel


class CreditRequestModel(BaseModel):
    accountId: int
    amount: int
    termMonths: int
