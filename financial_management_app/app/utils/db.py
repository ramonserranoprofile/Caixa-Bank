import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

import mysql.connector
from app.config import Config


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DB"),
    )
