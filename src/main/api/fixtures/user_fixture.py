import pytest
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_credit_user_request import CreateCreditUserRequest
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.models.transfer_funds_request import TransferFundsRequest
from src.main.api.models.account_deposit_request import AccountDepositRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_request_model import CreditRequestModel
from src.main.api.models.create_user_request import CreateUserRequest


@pytest.fixture
def create_user(api_manager):
    # Создаем обычного пользователя (ROLE_USER).
    create_user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(create_user_request)
    return create_user_request


@pytest.fixture
def create_account(api_manager, create_user):
    # Создаем банковский счет для обычного пользователя (create_user).
    account = api_manager.user_steps.create_account(create_user)

    account_deposit_request = AccountDepositRequest(accountId=account.id, amount=1500)
    return account_deposit_request


@pytest.fixture
def create_transfer_funds_accounts(api_manager, create_user):
    accounts = []

    # В цикле создаем два аккаунта для осуществления перевода между ними.
    # Id аккаунтов записываются в переменную "accounts".
    for _ in range(2):
        response = api_manager.user_steps.create_account(create_user)
        accounts.append(response.id)

    # Пополняем баланс аккаунта №1.
    account_deposit_request = AccountDepositRequest(accountId=accounts[0], amount=1500)
    api_manager.user_steps.account_deposit_request(create_user, account_deposit_request)

    transfer_funds_request = TransferFundsRequest(fromAccountId=accounts[0], toAccountId=accounts[1], amount=500)
    return transfer_funds_request


@pytest.fixture
def create_credit_user(api_manager):
    # Создаем пользователя для кредитного счета (ROLE_CREDIT_SECRET).
    create_user_request = RandomModelGenerator.generate(CreateCreditUserRequest)
    api_manager.admin_steps.create_user(create_user_request)
    return create_user_request


@pytest.fixture
def credit_user_details(api_manager, create_credit_user):
    user_details = CreateUserResponse(
        id=create_credit_user.id,
        username=create_credit_user.username,
        password=create_credit_user.password,
        role=create_credit_user.role
    )
    return user_details


@pytest.fixture
def create_credit_account_request(api_manager, create_credit_user):
    # Создаем банковский счет используя кредитный аккаунт (create_credit_user)
    create_credit_account = api_manager.user_steps.create_account(create_credit_user)

    return create_credit_account


@pytest.fixture
def credit_request_details(api_manager, create_credit_user, create_credit_account_request):
    credit_request_model = CreditRequestModel(accountId=create_credit_account_request.id, amount=5000, termMonths=12)
    return credit_request_model


@pytest.fixture
def create_credit_request(api_manager, create_credit_user, credit_request_details):
    create_credit = api_manager.user_steps.valid_credit_request(create_credit_user, credit_request_details)

    return create_credit


@pytest.fixture
def credit_repay_details(api_manager, credit_user_details, create_credit_request):
    repay_details = CreditRepayRequest(
        creditId= create_credit_request.creditId,
        accountId=create_credit_request.accountId,
        amount=5000
    )
    return repay_details
