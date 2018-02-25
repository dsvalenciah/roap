
"""
Contains user Exceptions.
"""


class RoapError(Exception):
    """Encapsulates our exceptions."""


class UserNotFoundError(RoapError):
    """A definition is not well defined."""


class UserSchemaError(RoapError):
    """A definition is not well defined."""


class UserUnmodifyError(RoapError):
    """A definition is not well defined."""


class UserUndeleteError(RoapError):
    """A definition is not well defined."""


class UserDuplicateEmailError(RoapError):
    """A definition is not well defined."""
