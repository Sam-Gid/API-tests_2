from src.main.api.requests.trunsfer_funds_requester import TransferFundsRequester
from src.main.api.requests.deposit_account_requester import DepositAccountRequester
from src.main.api.requests.create_account_requester import CreateAccountRequester
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.models.transfer_funds_request import TransferFundsRequest
from src.main.api.models.create_user_request import CreateUserRequest


class TestTransferFunds:
    def test_valid_transfer_funds(self):
        create_user_request = CreateUserRequest(username='Sam92', password='Pas!sw0rd', role='ROLE_USER')
        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username='admin', password='123456'),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        accounts = []

        # В цикле создаем два аккаунта для осуществления перевода между ними.
        # Id аккаунтов записываются в переменную "accounts".
        for _ in range(2):
            response = CreateAccountRequester(
                request_spec=RequestSpecs.auth_headers(username='Sam92', password='Pas!sw0rd'),
                response_spec=ResponseSpecs.request_created()
            ).post(None)

            accounts.append(response.id)

        account_one_id, account_two_id = accounts[0], accounts[1]

        deposit_account_request = DepositAccountRequest(accountId=account_one_id, amount=1000.5)

        DepositAccountRequester(
            request_spec=RequestSpecs.auth_headers(username='Sam92', password='Pas!sw0rd'),
            response_spec=ResponseSpecs.request_ok()
        ).post(deposit_account_request)

        transfer_funds_request = TransferFundsRequest(fromAccountId=account_one_id, toAccountId=account_two_id,
                                                      amount=500.5)

        response = TransferFundsRequester(
            request_spec=RequestSpecs.auth_headers(username='Sam92', password='Pas!sw0rd'),
            response_spec=ResponseSpecs.request_ok()
        ).post(transfer_funds_request)

        assert response.fromAccountIdBalance == 500


    def test_transfer_founds_with_invalid_amount(self):
        create_user_request = CreateUserRequest(username='Sam93', password='Pas!sw0rd', role='ROLE_USER')
        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username='admin', password='123456'),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        accounts = []

        # В цикле создаем два аккаунта для осуществления перевода между ними.
        # Id аккаунтов записываются в переменную "accounts".
        for _ in range(2):
            response = CreateAccountRequester(
                request_spec=RequestSpecs.auth_headers(username='Sam93', password='Pas!sw0rd'),
                response_spec=ResponseSpecs.request_created()
            ).post(None)

            accounts.append(response.id)

        account_one_id, account_two_id = accounts[0], accounts[1]

        deposit_account_request = DepositAccountRequest(accountId=account_one_id, amount=1000.5)

        DepositAccountRequester(
            request_spec=RequestSpecs.auth_headers(username='Sam93', password='Pas!sw0rd'),
            response_spec=ResponseSpecs.request_ok()
        ).post(deposit_account_request)

        boundary_values = [499, 10001]

        # Проверяем, что суммы перевода ниже минимума и выше максимума отклоняются.
        for i in range(2):
            transfer_funds_request = TransferFundsRequest(fromAccountId=account_one_id, toAccountId=account_two_id,
                                                          amount=boundary_values[i])

            response = TransferFundsRequester(
                request_spec=RequestSpecs.auth_headers(username='Sam93', password='Pas!sw0rd'),
                response_spec=ResponseSpecs.request_bad()
            ).post(transfer_funds_request)

            assert response.status_code == 400
