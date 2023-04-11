import string
from dataclasses import dataclass
from abc import ABC, abstractmethod
from random import choices, randint


@dataclass
class Account:
    email: str
    password: str


def generate_email() -> str:
    email = choices(string.ascii_lowercase, k=randint(8, 15))
    return ''.join(email) + '@gmail.com'


def generate_password() -> str:
    password = choices(string.printable, k=15)
    return ''.join(password)


class IAccountRepository(ABC):

    @abstractmethod
    def add(self, account: Account) -> None:
        raise NotImplementedError()

    @abstractmethod
    def all(self) -> list[Account]:
        raise NotImplementedError()
