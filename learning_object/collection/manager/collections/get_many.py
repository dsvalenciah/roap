def get_many(db_client):
    cursor = db_client.collections.find()
    collections = list(cursor)

    return collections