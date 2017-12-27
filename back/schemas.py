from apistar import typesystem


class User(typesystem.Object):
    properties = {
        "_id": typesystem.string(max_length=40),
        "name": typesystem.string(max_length=50),
        "email": typesystem.string(max_length=50),
    }


class Publication(typesystem.Object):
    properties = {
        '_id': typesystem.string(max_length=40),
        'title': typesystem.string(max_length=512),
        'description': typesystem.string(max_length=float('inf')),
    }