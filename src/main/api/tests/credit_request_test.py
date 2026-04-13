

class TestCreditRequest:
    def test_valid_credit_request(self, api_manager, create_credit_user, credit_request_details):
        response = api_manager.user_steps.valid_credit_request(create_credit_user, credit_request_details)

        assert response.balance == 5000

    def test_credit_request_without_permission(self, api_manager, create_user, credit_request_details):

        # Используем пользователя без права на кредитование (create_user).
        response = api_manager.user_steps.invalid_role_credit_request(create_user, credit_request_details)

        assert response.status_code == 403

    def test_credit_request_with_invalid_amount(self, api_manager, create_credit_user, credit_request_details):

        # Проверяем, что суммы кредита ниже минимума и выше максимума отклоняются.
        credit_amounts = [4999, 15001]
        for invalid_amount in credit_amounts:
            credit_request_details.amount = invalid_amount
            response = api_manager.user_steps.invalid_amount_credit_request(create_credit_user, credit_request_details)

            assert response.status_code == 400




