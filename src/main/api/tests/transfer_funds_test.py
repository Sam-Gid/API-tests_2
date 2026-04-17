import pytest
from sqlalchemy.orm import Session

from src.main.api.db.crud.account_crud import AccountCrudDb as Account


class TestTransferFunds:
    def test_valid_transfer_funds(self, api_manager, create_user_request, transfer_funds_request, db_session: Session):
        response = api_manager.user_steps.transfer_funds_request(create_user_request, transfer_funds_request)
        assert response.fromAccountIdBalance == 1000

        account1_from_db = Account.get_account_by_id(db_session, response.fromAccountId)
        account2_from_db = Account.get_account_by_id(db_session, response.toAccountId)
        print(account1_from_db.balance)
        print(account2_from_db.balance)


    @pytest.mark.parametrize(
        "fund_amount",
        [499, 10001]
    )
    def test_transfer_funds_with_invalid_amount(self, api_manager, create_user_request, transfer_funds_request, fund_amount):
        # Проверяем, что суммы перевода ниже минимума и выше максимума отклоняются.
        transfer_funds_request.amount = fund_amount
        response = api_manager.user_steps.invalid_transfer_funds_request(create_user_request, transfer_funds_request)
        assert response.status_code == 400
