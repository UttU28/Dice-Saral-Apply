# config/config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DATABASE_CONFIG = {
    'server': os.getenv('DB_SERVER'),
    'database': os.getenv('DB_DATABASE'),
    'username': os.getenv('DB_USERNAME'),
    'password': os.getenv('DB_PASSWORD'),
}
