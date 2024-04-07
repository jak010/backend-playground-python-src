import os
from enum import Enum

from dotenv import load_dotenv

load_dotenv()


class TMDBConfig(Enum):
    TMDB_API_READ_KEY = os.environ['TMDB_API_READ_KEY']
