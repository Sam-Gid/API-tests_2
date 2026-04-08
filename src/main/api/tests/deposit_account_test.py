import requests


class TestDepositAccount:
    def test_valid_deposit_account(self):
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
                'username': 'Max49',
                'password': 'Pas!sw0rd',
                'role': 'ROLE_USER'
            },
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}'
            }
        )

        assert create_user_response.status_code == 200

        login_user_response = requests.post(
            url='http://localhost:4111/api/auth/token/login',
            json={
                'username': 'Max49',
                'password': 'Pas!sw0rd'
            },
            headers={
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }
        )

        assert login_user_response.status_code == 200
        token = login_user_response.json().get('token')

        create_account_response = requests.post(
            url='http://localhost:4111/api/account/create',
            headers={
                'accept': 'application/json',
                'Authorization': f'Bearer {token}'
            }
        )

        assert create_account_response.status_code == 201
        assert create_account_response.json().get('balance') == 0

        account_id = create_account_response.json().get('id')

        deposit_account_response = requests.post(
            url='http://localhost:4111/api/account/deposit',
            json={
                'accountId': account_id,
                'amount': 1000.5
            },
            headers={
                'accept': 'application/json',
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
        )

        assert deposit_account_response.status_code == 200
        assert deposit_account_response.json().get('balance') == 1000.5


    def test_deposit_account_with_invalid_amount(self):
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
                'username': 'Max55',
                'password': 'Pas!sw0rd',
                'role': 'ROLE_USER'
            },
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}'
            }
        )

        assert create_user_response.status_code == 200

        login_user_response = requests.post(
            url='http://localhost:4111/api/auth/token/login',
            json={
                'username': 'Max55',
                'password': 'Pas!sw0rd'
            },
            headers={
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }
        )

        assert login_user_response.status_code == 200
        token = login_user_response.json().get('token')

        create_account_response = requests.post(
            url='http://localhost:4111/api/account/create',
            headers={
                'accept': 'application/json',
                'Authorization': f'Bearer {token}'
            }
        )

        assert create_account_response.status_code == 201
        assert create_account_response.json().get('balance') == 0

        account_id = create_account_response.json().get('id')

        boundary_values = [999, 9001]
        for i in range(2):

            # Проверяем, что суммы пополнения ниже минимума и выше максимума отклоняются

            deposit_account_response = requests.post(
                url='http://localhost:4111/api/account/deposit',
                json={
                    'accountId': account_id,
                    'amount': boundary_values[i]
                },
                headers={
                    'accept': 'application/json',
                    'Authorization': f'Bearer {token}',
                    'Content-Type': 'application/json'
                }
            )

            assert deposit_account_response.status_code == 400
            assert deposit_account_response.json().get('error') == 'Amount must be between 1000 and 9000'

