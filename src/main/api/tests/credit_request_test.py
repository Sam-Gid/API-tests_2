import pytest
from http import HTTPStatus
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.models.credit_table import Credit
from src.main.api.models.create_credit_user_request import CreateCreditUserRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_request_model import CreditRequestModel


class TestCreditRequest:
    def test_valid_credit_request(
            self,
            api_manager: ApiManager,
            create_credit_user_request: CreateCreditUserRequest,
            credit_request_details: CreditRequestModel,
            db_session: Session
    ):
        response = api_manager.user_steps.valid_credit_request(create_credit_user_request, credit_request_details)
        assert response.balance == credit_request_details.amount, 'Ошибка: Баланс кредитного счета не пополнен'

        credit_from_db = db_session.query(Credit).filter(Credit.id == response.creditId).first()
        assert credit_from_db is not None, 'Ошибка: Запись о кредите не обнаружена в БД'
        assert credit_from_db.amount == response.amount, 'Ошибка: Запись о сумме запроса не кредит не обнаружена в БД'


    def test_credit_request_without_permission(
            self,
            api_manager: ApiManager,
            create_user_request: CreateUserRequest,
            credit_request_details: CreditRequestModel,
            db_session: Session
    ):
        # Используем пользователя без права на кредитование (create_user).
        response = api_manager.user_steps.invalid_role_credit_request(create_user_request, credit_request_details)
        assert response.status_code == HTTPStatus.FORBIDDEN, (
            f'Ошибка: Неправильный статус код. '
            f'Ожидалось: {HTTPStatus.FORBIDDEN}, получено: {response.status_code}'
        )


        credit_from_db = db_session.query(Credit).filter(Credit.account_id == credit_request_details.accountId).first()
        assert credit_from_db is None, (
                'Ошибка: Запись о кредите на пользователя без права на кредитование обнаружена в БД'
        )


    @pytest.mark.parametrize(
        "credit_amount",
        [4999, 15001]
    )
    def test_credit_request_with_invalid_amount(
            self,
            api_manager: ApiManager,
            create_credit_user_request: CreateCreditUserRequest,
            credit_request_details: CreditRequestModel,
            credit_amount: int,
            db_session: Session
    ):
        # Проверяем, что суммы кредита ниже минимума и выше максимума отклоняются.
        credit_request_details.amount = credit_amount
        response = api_manager.user_steps.invalid_amount_credit_request(create_credit_user_request, credit_request_details)
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'Ошибка: Неправильный статус код. '
            f'Ожидалось: {HTTPStatus.BAD_REQUEST}, получено: {response.status_code}'
        )

        credit_from_db = db_session.query(Credit).filter(Credit.account_id == credit_request_details.accountId).first()
        assert credit_from_db is None, 'Ошибка, запись о кредите на невалидную сумму найдена в БД'