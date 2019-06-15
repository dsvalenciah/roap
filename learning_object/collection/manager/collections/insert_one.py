from manager.schemas.learning_object import Collection
from uuid import uuid4

def insert_one(db_client, collection_name):
    collection_id = str(uuid4())
    collection_dict = dict(
        _id=collection_id,
        name=collection_name
    )

    collection, errors = Collection().dump(collection_dict)

    if errors:
        print(errors)
        print("ERORRRRRR!")
    
    result = db_client.collections.isnert_one(collection)

    return result.inserted_id