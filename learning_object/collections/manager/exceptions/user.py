
class RoapError(Exception):
    """Encapsulates our exceptions."""


class UserNotFoundError(RoapError):
    """A definition is not well defined."""


class UserPermissionError(RoapError):
    """A definition is not well defined."""
