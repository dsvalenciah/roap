
"""
Contains learning object Exceptions.
"""


class RoapError(Exception):
    """Encapsulates our exceptions."""


class LearningObjectNotFoundError(RoapError):
    """A definition is not well defined."""


class LearningObjectSchemaError(RoapError):
    """A definition is not well defined."""


class LearningObjectUnmodifyError(RoapError):
    """A definition is not well defined."""


class LearningObjectUndeleteError(RoapError):
    """A definition is not well defined."""


class LearningObjectFormatError(RoapError):
    """A definition is not well defined."""


class LearningObjectMetadataSchemaError(RoapError):
    """A definition is not well defined."""

class InvalidUserRaterRole(RoapError):
    """A definition is not well defined."""

class InvalidRatingValue(RoapError):
    """A definition is not well defined."""

class UserCannotRate(RoapError):
    """docstring for UserCannotRate"""

class LearningObjectFileNotFound(RoapError):
    """docstring for UserCannotRate"""
