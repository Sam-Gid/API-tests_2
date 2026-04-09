from src.main.api.requests.credit_requester import CreditRequester
from src.main.api.requests.create_account_requester import CreateAccountRequester
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.models.credit_request_model import CreditRequestModel
from src.main.api.models.create_user_request import CreateUserRequest


class TestCreditRequest:
    def test_create_account(self):
        create_user_request = CreateUserRequest(username='Sam36', password='Pas!sw0rd', role='ROLE_CREDIT_SECRET')

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username='admin', password='123456'),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username='Sam36', password='Pas!sw0rd'),
            response_spec=ResponseSpecs.request_created()
        ).post(None)
        account_id = response.id

        credit_request_model = CreditRequestModel(accountId=account_id, amount=5000, termMonths=12)

        response = CreditRequester(
            request_spec=RequestSpecs.auth_headers(username='Sam36', password='Pas!sw0rd'),
            response_spec=ResponseSpecs.request_created()
        ).post(credit_request_model)

        assert response.balance == 5000
        assert response.termMonths == 12


    def test_credit_request_without_permission(self):

        # Создаем пользователся без права на кредитование (ROLE_USER).
        create_user_request = CreateUserRequest(username='Sam37', password='Pas!sw0rd', role='ROLE_USER')

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username='admin', password='123456'),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username='Sam37', password='Pas!sw0rd'),
            response_spec=ResponseSpecs.request_created()
        ).post(None)
        account_id = response.id

        credit_request_model = CreditRequestModel(accountId=account_id, amount=5000, termMonths=12)

        response = CreditRequester(
            request_spec=RequestSpecs.auth_headers(username='Sam37', password='Pas!sw0rd'),
            response_spec=ResponseSpecs.request_forbidden()
        ).post(credit_request_model)

        assert response.status_code == 403


    def test_credit_request_with_invalid_amount(self):
        create_user_request = CreateUserRequest(username='Sam39', password='Pas!sw0rd', role='ROLE_CREDIT_SECRET')

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username='admin', password='123456'),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username='Sam39', password='Pas!sw0rd'),
            response_spec=ResponseSpecs.request_created()
        ).post(None)
        account_id = response.id

        boundary_values = [4999, 15001]

        # Проверяем, что суммы кредита ниже минимума и выше максимума отклоняются.
        for i in range(2):
            credit_request_model = CreditRequestModel(accountId=account_id, amount=boundary_values[i], termMonths=12)

            response = CreditRequester(
                request_spec=RequestSpecs.auth_headers(username='Sam39', password='Pas!sw0rd'),
                response_spec=ResponseSpecs.request_bad()
            ).post(credit_request_model)

            assert response.status_code == 400




