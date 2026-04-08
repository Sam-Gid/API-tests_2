from src.main.api.models.base_model import BaseModel


class CreditRequestResponse(BaseModel):
    creditId: int
    amountDeposited: float