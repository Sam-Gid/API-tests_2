from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from sqlalchemy.orm import Session
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.get_transactions_response import Transactions


def get_db_balance(db_session: Session, account_id: int) -> float:
    return Account.get_account_by_id(db_session, account_id).balance


def get_last_transaction(
        api_manager: ApiManager,
        create_user_request: CreateUserRequest,
        account_id: int
) -> Transactions:
    return api_manager.user_steps.get_last_transaction(create_user_request, account_id)