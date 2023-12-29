from typing import Optional

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from spotify_bot.database import db


class Base(DeclarativeBase):
    pass


class Account(Base):
    __tablename__ = "accounts"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    password: Mapped[str]


class Command(Base):
    __tablename__ = "commands"
    id: Mapped[int] = mapped_column(primary_key=True)
    playlist_url: Mapped[str]
    song_index: Mapped[Optional[int]]
    amount: Mapped[int]


Base.metadata.create_all(db)
