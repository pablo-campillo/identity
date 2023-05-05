"""Exceptions of the Service Layer for managing Users"""


class UserAlreadyExistsException(Exception):
    """A user with the same email already exists."""
    pass


class UserDoesNotExistException(Exception):
    """A user with a given email does not exists."""
    pass


class InvalidEmailFormatException(Exception):
    """The format of the email is not valid."""
    pass
