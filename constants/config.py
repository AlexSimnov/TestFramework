from dotenv import load_dotenv
from os import getenv

load_dotenv()

USERNAME_DB = getenv("DB_USERNAME")
PASSWORD_DB = getenv("DB_PASSWORD")
HOST_DB = getenv("DB_HOST")
PORT_DB = getenv("DB_PORT")
DATABASE_NAME_DB = getenv("DB_DATABASE_NAME")
