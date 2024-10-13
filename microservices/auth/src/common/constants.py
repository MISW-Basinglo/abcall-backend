import os
from enum import Enum

JWT_ACCESS_TOKEN_EXPIRES = os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 900)
JWT_REFRESH_TOKEN_EXPIRES = os.getenv("JWT_REFRESH_TOKEN_EXPIRES", 2592000)
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_jwt_secret_key")
JWT_ACCESS_DELTA = os.getenv("JWT_ACCESS_DELTA", 1)
JWT_REFRESH_DELTA = os.getenv("JWT_REFRESH", 30)
DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

if all([DATABASE_HOST, DATABASE_PORT, DATABASE_NAME, DATABASE_USER]):
    DATABASE_URI = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
else:
    DATABASE_URI = "sqlite:///local.db"


class ExceptionsMessages(str, Enum):
    USER_NOT_REGISTERED = "User not registered."
    INVALID_PASSWORD = "Invalid password."
    USER_NOT_AUTHORIZED = "User not authorized."
    USER_NOT_FOUND = "User not found."
    TOKEN_NOT_FOUND = "Token not found."
    RESOURCE_NOT_FOUND = "Resource not found."
    RESOURCE_EXISTS = "Resource already exists."
    INVALID_PARAMETER = "Invalid parameter."
    ERROR = "Something went wrong. Please try again later."
    ERROR_DECODING_TOKEN = "Error decoding token."
