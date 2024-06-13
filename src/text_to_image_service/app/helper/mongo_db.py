from pymongo import MongoClient
import gridfs


class MongoDBClient:
    def __init__(self, uri, db_name='t2m_images'):
        self.client = MongoClient(uri)
        # e.g., self.client.mydatabase if your DB name is `mydatabase`
        self.db = self.client[db_name]
        self.fs_db = gridfs.GridFS(self.db)

    def get_collection(self, collection_name):
        return self.db[collection_name]
