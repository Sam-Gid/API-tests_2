from src.main.api.requests.credit_repay_requester import CreditRepayRequester
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.requests.credit_requester import CreditRequester
from src.main.api.requests.create_account_requester import CreateAccountRequester
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_request_model import CreditRequestModel



class TestCreditRepay:
    def test_credit_repay(self):
        create_user_request = CreateUserRequest(username='Sam82', password='Pas!sw0rd', role='ROLE_CREDIT_SECRET')

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username='admin', password='123456'),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username='Sam82', password='Pas!sw0rd'),
            response_spec=ResponseSpecs.request_created()
        ).post(None)
        account_id = response.id

        credit_request_model = CreditRequestModel(accountId=account_id, amount=5000, termMonths=12)

        response = CreditRequester(
            request_spec=RequestSpecs.auth_headers(username='Sam82', password='Pas!sw0rd'),
            response_spec=ResponseSpecs.request_created()
        ).post(credit_request_model)

        assert response.balance == 5000
        assert response.termMonths == 12

        credit_id = response.creditId

        credit_repay_request = CreditRepayRequest(creditId=credit_id, accountId=account_id, amount=5000)

        response = CreditRepayRequester(
            request_spec=RequestSpecs.auth_headers(username='Sam82', password='Pas!sw0rd'),
            response_spec=ResponseSpecs.request_ok()
        ).post(credit_repay_request)

        assert response.amountDeposited == 5000


    def test_credit_repay_with_invalid_amount(self):
        create_user_request = CreateUserRequest(username='Sam83', password='Pas!sw0rd', role='ROLE_CREDIT_SECRET')

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username='admin', password='123456'),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username='Sam83', password='Pas!sw0rd'),
            response_spec=ResponseSpecs.request_created()
        ).post(None)
        account_id = response.id

        credit_request_model = CreditRequestModel(accountId=account_id, amount=5000, termMonths=12)

        response = CreditRequester(
            request_spec=RequestSpecs.auth_headers(username='Sam83', password='Pas!sw0rd'),
            response_spec=ResponseSpecs.request_created()
        ).post(credit_request_model)

        assert response.balance == 5000
        assert response.termMonths == 12

        credit_id = response.creditId

        boundary_values = [4999, 5001]

        # Проверяем, что суммы пополнений, которые не равны сумме кредита, отклоняются.
        for i in range(2):
            credit_repay_request = CreditRepayRequest(creditId=credit_id, accountId=account_id, amount=boundary_values[i])

            response = CreditRepayRequester(
                request_spec=RequestSpecs.auth_headers(username='Sam83', password='Pas!sw0rd'),
                response_spec=ResponseSpecs.request_unprocessable()
            ).post(credit_repay_request)

            assert response.status_code == 422


    def test_repay_closed_credit(self):
        create_user_request = CreateUserRequest(username='Sam84', password='Pas!sw0rd', role='ROLE_CREDIT_SECRET')

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username='admin', password='123456'),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username='Sam84', password='Pas!sw0rd'),
            response_spec=ResponseSpecs.request_created()
        ).post(None)
        account_id = response.id

        credit_request_model = CreditRequestModel(accountId=account_id, amount=5000, termMonths=12)

        response = CreditRequester(
            request_spec=RequestSpecs.auth_headers(username='Sam84', password='Pas!sw0rd'),
            response_spec=ResponseSpecs.request_created()
        ).post(credit_request_model)

        assert response.balance == 5000
        assert response.termMonths == 12

        credit_id = response.creditId

        credit_repay_request = CreditRepayRequest(creditId=credit_id, accountId=account_id, amount=5000)

        expected_responses = [
            ResponseSpecs.request_ok(),
            ResponseSpecs.request_unprocessable(),
        ]

        # Проверяем, что при повторном погашении кредита получаем ошибку.
        for i in range(2):
            response = CreditRepayRequester(
                request_spec=RequestSpecs.auth_headers(username='Sam84', password='Pas!sw0rd'),
                response_spec=expected_responses[i]
            ).post(credit_repay_request)

        assert response.status_code == 422


