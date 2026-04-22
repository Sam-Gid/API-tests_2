import pytest
from sqlalchemy.orm import Session
from src.main.api.db.crud.account_crud import AccountCrudDb as Account


class TestTransferFunds:
    def test_valid_transfer_funds(
            self,
            api_manager,
            create_user_request,
            transfer_funds_request,
            funded_account,
            db_session: Session
    ):
        sender_balance_before = Account.get_account_by_id(db_session, transfer_funds_request.fromAccountId).balance
        recipient_balance_before = Account.get_account_by_id(db_session, transfer_funds_request.toAccountId).balance

        response = api_manager.user_steps.transfer_funds_request(create_user_request, transfer_funds_request)

        # Получаем последние транзакции отправителя и получателя.
        sender_transaction =  api_manager.user_steps.get_last_transaction(create_user_request, response.fromAccountId)
        recipient_transaction = api_manager.user_steps.get_last_transaction(create_user_request, response.toAccountId)
        assert sender_transaction.amount == -transfer_funds_request.amount
        assert recipient_transaction.amount == transfer_funds_request.amount

        sender_balance_after = Account.get_account_by_id(db_session, transfer_funds_request.fromAccountId).balance
        recipient_balance_after = Account.get_account_by_id(db_session, transfer_funds_request.toAccountId).balance
        assert transfer_funds_request.amount == sender_balance_before - sender_balance_after
        assert transfer_funds_request.amount == recipient_balance_after - recipient_balance_before


    @pytest.mark.parametrize(
        "transfer_amount",
        [499, 10001]
    )
    def test_transfer_funds_with_invalid_amount(
            self,
            api_manager,
            create_user_request,
            transfer_funds_request,
            funded_account,
            transfer_amount,
            db_session: Session):
        # Проверяем, что суммы перевода ниже минимума и выше максимума отклоняются.
        funded_account_balance = funded_account.balance
        transfer_funds_request.amount = transfer_amount

        response = api_manager.user_steps.invalid_transfer_funds_request(create_user_request, transfer_funds_request)
        assert response.status_code == 400, f'Ожидался статус-код: 400, получен: {response.status_code}'

        source_account = Account.get_account_by_id(db_session, transfer_funds_request.fromAccountId)
        target_account = Account.get_account_by_id(db_session, transfer_funds_request.toAccountId)

        assert source_account.balance == funded_account_balance, (
            f'Ошибка: Баланс отправителя изменился после перевода невалидной суммы. '
            f'Ожидалось: {funded_account_balance}, получено: {source_account.balance}'
        )
        assert target_account.balance == 0, (
            f'Ошибка: Баланс получателя изменился после невалидного перевода. '
            f'Ожидалось: 0, получено: {target_account.balance}'
        )