from spotify_bot.repositories import AccountRepository
from spotify_bot.use_cases import register, create_driver
from spotify_bot.domain import generate_email, generate_password, Account


if __name__ == '__main__':
    amount = int(input('Quantas contas deseja criar? '))
    driver = create_driver()
    account_repository = AccountRepository()
    for i in range(amount):
        email = generate_email()
        password = generate_password()
        registered = register(driver, email, password)
        if registered:
            account_repository.add(Account(email, password))
