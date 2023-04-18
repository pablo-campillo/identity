import pytest

from datetime import datetime, timedelta
from identity.domain.users import User


def new_user(active=False):
    email = 'petete@version1.com'
    pw = 'password'
    return User(email=email, password=pw, active=active)


def test_new_user():
    now = datetime.utcnow()
    a_second_later = now + timedelta(seconds=1)

    email = 'petete@version1.com'
    pw = 'password'
    user = User(email=email, password=pw)

    assert user.email == email
    assert user.password == pw
    assert not user.is_validated()
    assert not user.is_active()
    assert now <= user.created_at  <= a_second_later
    assert now <= user.updated_at <= a_second_later


def test_validate_user():
    user = new_user()
    now = datetime.utcnow()
    user.validate()

    assert user.is_validated()
    assert user.updated_at >= now


def test_enable_user():
    user = new_user()
    now = datetime.utcnow()
    user.enable()

    assert user.is_active()
    assert user.updated_at >= now


def test_disable_user():
    user = new_user(active=True)
    now = datetime.utcnow()
    user.enable()

    assert user.is_active()
    assert user.updated_at >= now
