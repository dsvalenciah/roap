class RoapError(Exception):
    """Encapsulates our exceptions."""


class SubCollectionNotFoundError(RoapError):
    """A definition is not well defined."""


class SubCollectionSchemaError(RoapError):
    """A definition is not well defined."""


class SubCollectionUnmodifyError(RoapError):
    """A definition is not well defined."""


class SubCollectionUndeleteError(RoapError):
    """A definition is not well defined."""


class SubCollectionFormatError(RoapError):
    """A definition is not well defined."""
