import re

from spotify_bot.domain import generate_email


def test_generate_email() -> None:
    regex = re.compile(
        r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    assert regex.findall(generate_email())
