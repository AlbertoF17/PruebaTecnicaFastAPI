import pymongo

class MongoDBManager:
    def __init__(self, connection_string, database_name, collection_name):
        self.client = pymongo.MongoClient(connection_string)
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]

    def insert_data(self, data_dict):
        self.collection.delete_many({})
        self.collection.insert_many(data_dict)

    def get_total_consumption(self):
        consumo_total = self.collection.aggregate([{"$group": {"_id": None, "total_consumption": {"$sum": "$Energy (kWh)"}}}])[0]["total_consumption"]
        return consumo_total

    def get_consumption_by_date(self, fecha):
        datos_fecha = self.collection.find({"Date": fecha})
        consumo_fecha = sum(doc["Energy (kWh)"] for doc in datos_fecha)
        return consumo_fecha