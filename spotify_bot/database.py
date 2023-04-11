from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

from spotify_bot.models import Base


load_dotenv()

db = create_engine(os.getenv('SQLALCHEMY_DATABASE_URI'))
Session = sessionmaker(db)
Base.metadata.create_all(db)
