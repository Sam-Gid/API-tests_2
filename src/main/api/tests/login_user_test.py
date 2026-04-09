import pytest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.requests.login_user_requester import LoginUserRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


@pytest.mark.api
class TestUserLogin:
    def test_login_user(self):
        create_user_request = CreateUserRequest(username='Sam21', password='Pas!sw0rd', role='ROLE_USER')

        response = CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username='admin', password='123456'),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        assert create_user_request.username == response.username
        assert create_user_request.role == response.role

        login_user_request = LoginUserRequest(username='Sam21', password='Pas!sw0rd')

        response = LoginUserRequester(
            request_spec=RequestSpecs.unauth_headers(),
            response_spec=ResponseSpecs.request_ok()
        ).post(login_user_request)

        assert login_user_request.username == response.user.username
