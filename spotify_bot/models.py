from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class AccountModel(Base):
    __tablename__ = 'accounts'
    email = Column(String, primary_key=True, nullable=False)
    password = Column(String, nullable=False)
