from src.main.api.requests.deposit_account_requester import DepositAccountRequester
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.requests.create_account_requester import CreateAccountRequester
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.models.create_user_request import CreateUserRequest



class TestDepositAccount:
    def test_valid_deposit_account(self):
        create_user_request = CreateUserRequest(username='Sam89', password='Pas!sw0rd', role='ROLE_USER')

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username='admin', password='123456'),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username='Sam89', password='Pas!sw0rd'),
            response_spec=ResponseSpecs.request_created()
        ).post(None)

        account_id = response.id

        deposit_account_request = DepositAccountRequest(accountId=account_id, amount=5000)

        response = DepositAccountRequester(
            request_spec=RequestSpecs.auth_headers(username='Sam89', password='Pas!sw0rd'),
            response_spec=ResponseSpecs.request_ok()
        ).post(deposit_account_request)

        assert response.balance == 5000


    def test_deposit_account_with_invalid_amount(self):
        create_user_request = CreateUserRequest(username='Sam90', password='Pas!sw0rd', role='ROLE_USER')

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username='admin', password='123456'),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username='Sam90', password='Pas!sw0rd'),
            response_spec=ResponseSpecs.request_created()
        ).post(None)

        account_id = response.id

        boundary_values = [999, 9001]

        # Проверяем, что суммы пополнения ниже минимума и выше максимума отклоняются.
        for i in range(2):
            deposit_account_request = DepositAccountRequest(accountId=account_id, amount=boundary_values[i])

            response = DepositAccountRequester(
                request_spec=RequestSpecs.auth_headers(username='Sam90', password='Pas!sw0rd'),
                response_spec=ResponseSpecs.request_bad()
            ).post(deposit_account_request)

            assert response.status_code == 400
