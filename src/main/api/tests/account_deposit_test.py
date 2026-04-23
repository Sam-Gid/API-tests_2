import pytest
from http import HTTPStatus
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.helpers.account_helpers import get_db_balance
from src.main.api.models.account_deposit_request import AccountDepositRequest
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest


class TestDepositAccount:
    def test_valid_deposit_account(
            self,
            api_manager: ApiManager,
            create_user_request: CreateUserRequest,
            account_deposit_request: AccountDepositRequest,
            db_session: Session
    ):
        amount = account_deposit_request.amount
        account_id = account_deposit_request.accountId

        account_db_balance_before = get_db_balance(db_session, account_id)

        response = api_manager.user_steps.account_deposit_request(create_user_request, account_deposit_request)
        assert response.balance == amount, 'Ошибка: Баланс аккаунта не пополнен'

        account_db_balance_after = get_db_balance(db_session, account_id)
        assert account_db_balance_after == account_db_balance_before + amount, (
            f'Ошибка: Баланс аккаунта не пополнен. '
            f'Ожидалось: Поле "Баланс" в БД = {amount}, получено: {account_db_balance_after}'
        )


    @pytest.mark.parametrize(
        "deposit_amount",
        [999, 9001]
    )
    def test_deposit_account_with_invalid_amount(
            self,
            api_manager: ApiManager,
            create_user_request: CreateUserRequest,
            account_deposit_request: AccountDepositRequest,
            deposit_amount: int,
            create_account_response: CreateAccountResponse,
            db_session: Session
    ):
        # Проверяем, что суммы пополнения ниже минимума и выше максимума отклоняются.
        account_deposit_request.amount = deposit_amount

        account_id = account_deposit_request.accountId
        account_db_balance_before = get_db_balance(db_session, account_id)

        response = api_manager.user_steps.account_invalid_deposit_request(create_user_request, account_deposit_request)
        assert response.status_code == HTTPStatus.BAD_REQUEST

        account_db_balance_after = get_db_balance(db_session, account_id)
        assert account_db_balance_after == account_db_balance_before, (
            f'Ошибка: Баланс аккаунта в БД изменен. '
            f'Ожидалось: {account_db_balance_before}, получено: {account_db_balance_after}'
        )