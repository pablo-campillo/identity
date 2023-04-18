from decouple import config


def get_jwt_secret_key():
    return config('JWT_SECRET_KEY', default='MY_SECRET')


def get_jwt_algorithm():
    return config('JWT_ALGORITHM', default='HS256')


def get_jwt_access_tocken_expire_minutes():
    return int(config('JWT_ACCESS_TOKEN_EXPIRE_MINUTES', default=30))


def get_database_url():
    DB_USER = config("DB_USER")
    DB_PASSWORD = config("DB_PASSWORD")
    DB_DATABASE = config("DB_DATABASE")
    DB_HOST = config("DB_HOST")
    DB_PORT = config("DB_PORT")
    return f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
