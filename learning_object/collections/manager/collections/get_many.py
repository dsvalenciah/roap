def get_many(db_client):
    cursor = db_client.locollection.find()
    collections = list(cursor)

    return collections