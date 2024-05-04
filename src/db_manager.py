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
        # Execute the aggregation pipeline (assuming you want total consumption)
        cursor = self.collection.aggregate([{"$group": {"_id": None, "total_consumption": {"$sum": "$Energy (kWh)"}}}])

        # Convert the cursor to a list and get the first element (assuming there's only one document)
        data = list(cursor)
        if data:
            consumo_total = data[0]["total_consumption"]
        else:
            consumo_total = 0  # Handle the case where no data is found (optional)

        return consumo_total

    def get_consumption_by_date(self, fecha):
        # Find documents for the specified date
        datos_fecha = self.collection.find({"Date": fecha})

        # Sum the "Energy (kWh)" values for all matching documents
        consumo_fecha = sum(doc["Energy (kWh)"] for doc in datos_fecha)

        return consumo_fecha