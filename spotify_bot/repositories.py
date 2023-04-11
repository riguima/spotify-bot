from spotify_bot.domain import IAccountRepository, Account
from spotify_bot.database import Session
from spotify_bot.models import AccountModel


class AccountRepository(IAccountRepository):

    def add(self, account: Account) -> None:
        with Session() as session:
            session.add(AccountModel(email=account.email,
                                     password=account.password))
            session.commit()

    def all(self) -> list[Account]:
        with Session() as session:
            return [Account(m.email, m.password)
                    for m in session.query(AccountModel).all()]
