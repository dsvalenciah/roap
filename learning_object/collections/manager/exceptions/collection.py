class RoapError(Exception):
    """Encapsulates our exceptions."""


class CollectionNotFoundError(RoapError):
    """A definition is not well defined."""


class CollectionSchemaError(RoapError):
    """A definition is not well defined."""


class CollectionUnmodifyError(RoapError):
    """A definition is not well defined."""


class CollectionUndeleteError(RoapError):
    """A definition is not well defined."""


class CollectionFormatError(RoapError):
    """A definition is not well defined."""
