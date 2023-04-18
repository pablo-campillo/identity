# Introduction

This project aims at being a reference of how a Web API must be designed and implementd using Version 1 best practices.

**Core users** of this project are other **V1 Python Developers (V1PD)** who want to add a customizable Authentication and Authorization module to Web API projects. It is implemented using OAuth2 standard and FastAPI framework but it can be easily modified to use with other app web frameworks.

The main entity is the user who can be registered by themself or by another user who owns proper privileges.

## Web API User stories

As V1PD I want to **register a new user**.

# Requirements

## Poetry Installation

Type the following in a linux terminal:
```shell
curl -sSL https://install.python-poetry.org | python3 -
```

Update the PATH environment variable:
```shell
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
```

Logout and in and check poetry's version:

```shell
$ poetry --version
Poetry (version 1.4.2)
```

The project was created using the following command (use it just for new projects from scratch):

```shell
poetry new --src identity
```


# bitacora

```shell
poetry add fastapi
poetry add "uvicorn[standard]"
poetry add python-multipart
poetry add "python-jose[cryptography]"
poetry add "passlib[bcrypt]"
poetry add sqlalchemy[asyncio]
poetry add asyncpg
poetry add python-decouple
poetry add --group dev alembic
poetry add --group dev pytest
poetry add --group dev pytest-mock
poetry add --group dev httpx
```

## Alembic

```shell
alembic init -t async src/identity/adapters/db/migrations
```

```shell
alembic revision --autogenerate -m 'adds user table'
```