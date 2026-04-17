import pytest
from sqlalchemy.orm import Session
from src.main.api.db.models.credit_table import Credit


class TestCreditRepay:
    def test_credit_repay(
            self,
            api_manager,
            create_credit_user_request,
            credit_repay_request,
            db_session: Session
    ):
        response = api_manager.user_steps.credit_repay_request(create_credit_user_request, credit_repay_request)
        assert response.amountDeposited == 5000

        credit_from_db = db_session.query(Credit).filter(Credit.id == response.creditId).first()
        assert credit_from_db.balance == 0
        assert credit_from_db.amount == 5000


    @pytest.mark.parametrize(
        'repay_amount',
        [4999, 5001]
    )
    def test_credit_repay_with_invalid_amount(
            self,
            api_manager,
            create_credit_user_request,
            credit_repay_request,
            repay_amount,
            db_session: Session
    ):
        # Проверяем, что суммы пополнений, которые не равны сумме кредита, отклоняются.
        credit_repay_request.amount = repay_amount
        response = api_manager.user_steps.invalid_credit_repay_request(create_credit_user_request, credit_repay_request)
        assert response.status_code == 422

        credit_from_db = db_session.query(Credit).filter(Credit.id == credit_repay_request.creditId).first()
        assert credit_from_db.balance != 0


    def test_repay_closed_credit(
            self,
            api_manager,
            create_credit_user_request,
            credit_repay_request,
            db_session: Session
    ):
        # Проверяем, что при повторном погашении кредита получаем ошибку.
        response = api_manager.user_steps.credit_repay_request(create_credit_user_request, credit_repay_request)
        assert response.amountDeposited == credit_repay_request.amount

        credit_from_db = db_session.query(Credit).filter(Credit.id == response.creditId).first()
        assert credit_from_db.balance == 0
        assert credit_from_db.amount == credit_repay_request.amount

        response2 = api_manager.user_steps.invalid_credit_repay_request(create_credit_user_request, credit_repay_request)
        assert response2.status_code == 422

        credit_from_db = db_session.query(Credit).filter(Credit.id == credit_repay_request.creditId).first()
        assert credit_from_db.balance == 0, 'Ошибка, повторное погашение кредита'


