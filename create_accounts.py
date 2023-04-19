from spotify_bot.repositories import AccountRepository
from spotify_bot.use_cases import register, create_driver
from spotify_bot.domain import generate_email, Account


if __name__ == '__main__':
    amount = int(input('Quantas contas deseja criar? '))
    driver = create_driver(visible=True)
    account_repository = AccountRepository()
    for i in range(amount):
        email = generate_email()
        password = 'Ri12345678!'
        registered = register(driver, Account(email, password))
        if registered:
            account_repository.add(Account(email, password))
    driver.quit()
