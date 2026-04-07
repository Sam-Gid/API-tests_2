import requests
import pytest


@pytest.mark.api
class TestCreateUser:
    def test_create_user_valid(self):
        login_admin_response = requests.post(
            url='http://localhost:4111/api/auth/token/login',
            json={
                'username': 'admin',
                'password': '123456'
            },
            headers={
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }
        )

        assert login_admin_response.status_code == 200
        token = login_admin_response.json().get('token')

        create_user_response = requests.post(
            url='http://localhost:4111/api/admin/create',
            json={
                'username': 'Max36',
                'password': 'Pas!sw0rd',
                'role': 'ROLE_USER'
            },
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}'
            }
        )

        assert create_user_response.status_code == 200
        assert create_user_response.json().get('username') == 'Max36'
        assert create_user_response.json().get('role') == 'ROLE_USER'


    @pytest.mark.parametrize(
        'username, password',
        [
            ('Абг', 'Pas!sw0rd'),
            ('ab', 'Pas!sw0rd'),
            ('abv!', 'Pas!sw0rd'),
            ('Maxx1', 'Pas!sw0rд'),
            ('Maxx2', 'Pas!sw0'),
            ('Maxx3', 'pas!sw0rd'),
            ('Maxx4', 'PAS!SW0RD'),
            ('Maxx5', 'pasSsw0rd'),
            ('Maxx6', 'pasSsword'),
        ]
    )
    def test_create_user_invalid(self, username, password):
        login_admin_response = requests.post(
            url='http://localhost:4111/api/auth/token/login',
            json={
                'username': 'admin',
                'password': '123456'
            },
            headers={
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }
        )

        assert login_admin_response.status_code == 200
        token = login_admin_response.json().get('token')

        create_user_response = requests.post(
            url='http://localhost:4111/api/admin/create',
            json={
                'username': username,
                'password': password,
                'role': 'ROLE_USER'
            },
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}'
            }
        )

        assert create_user_response.status_code == 400



