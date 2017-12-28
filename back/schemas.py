import typing

from apistar import typesystem

class UserRoles(typesystem.Enum):
    enum=['administrator', 'expert', 'creator', 'external']

class PublicationRating(typesystem.Integer):
    minimum = 1
    maximum = 5

class PublicationType(typesystem.Enum):
    enum = ['zip', 'html']

class PublicationState(typesystem.Enum):
    enum = ['unevaluated', 'evaluated']

class Publication(typesystem.Object):
    properties = {
        '_id': typesystem.string(max_length=40),
        'title': typesystem.string(max_length=512),
        'description': typesystem.string(max_length=float('inf')),
        'expert_rating': PublicationRating,
        'general_rating': PublicationRating,
        'type': PublicationType,
        'files_path': typesystem.string(max_length=40),
        'tags': typesystem.array(),
        'state': PublicationState,
    }

class User(typesystem.Object):
    properties = {
        '_id': typesystem.string(max_length=40),
        'name': typesystem.string(max_length=50),
        'email': typesystem.string(max_length=50),
        'role': UserRoles,
        'created': typesystem.string(max_length=40),
        'modified': typesystem.string(max_length=40),
        'publications': typing.List[Publication],
    }
