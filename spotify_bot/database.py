from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from spotify_bot.config import get_config

db = create_engine(get_config()["DATABASE_URI"])
Session = sessionmaker(db)
