import pymongo
import pandas as pd

csv = "Data/Monitoring report.csv"

class MongoDBManager:
    def __init__(self, connection_string, database_name, collection_name):
        self.client = pymongo.MongoClient(connection_string)
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]

    def init_data(self):
        df = pd.read_csv(csv)
        data = df.to_dict(orient='records')
        self.insert_data(data)

    def insert_data(self, data_dict):
        self.collection.delete_many({})
        self.collection.insert_many(data_dict)

    def get_consumption_by_date(self, fecha):
        datos_fecha = self.collection.find({"Date": fecha})
        consumo_fecha = sum(doc["Energy (kWh)"] for doc in datos_fecha)
        return consumo_fecha