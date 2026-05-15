import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.models.create_user_request import CreateUserRequest


@pytest.mark.api
class TestCreateAccount:
    def test_create_account(
            self,
            api_manager: ApiManager,
            create_user_request: CreateUserRequest,
            db_session: Session
    ):
        response = api_manager.user_steps.create_account(create_user_request)
        assert response.balance == 0, f'Ошибка: Баланс аккаунта не равен нулю. Получено: {response.balance}'

        account_db = Account.get_account_by_id(db_session, response.id)
        assert account_db.id == response.id, 'Ошибка: id аккаунта не найден в БД'
        assert account_db.number == response.number, 'Ошибка: номер счета аккаунта не найден в БД'
        assert account_db.balance == 0, 'Ошибка: баланс аккаунта в БД не равен нулю'
