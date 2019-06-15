from ..schemas import SubCollection
from uuid import uuid4


def insert_one(db_client, collection_id, name_sub_collection):
    sub_collection_id = str(uuid4())
    sub_collection_dict = dict(
        _id=sub_collection_id,
        name=name_sub_collection,
        collection_id=collection_id
    )

    sub_collection, errors = SubCollection().dump(sub_collection_dict)

    if errors:
        print(errors)
        print("ERRORRRRRRR SUB_COLLECTION")
    
    result = db_client.sub_collection.insert_one(sub_collection)

    return result.inserted_id
