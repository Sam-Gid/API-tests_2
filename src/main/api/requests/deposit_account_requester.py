from http import HTTPStatus

import requests
from requests import Response
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.models.deposit_account_response import DepositAccountResponse
from src.main.api.requests.requester import Requester


class DepositAccountRequester(Requester):
    def post(self, deposit_account_request: DepositAccountRequest) -> DepositAccountResponse | Response:
        url = f'{self.base_url}/account/deposit'
        response = requests.post(
            url=url,
            json=deposit_account_request.model_dump(),
            headers=self.headers,
        )
        self.response_spec(response)

        if response.status_code == HTTPStatus.OK:
            return DepositAccountResponse(**response.json())
        return response