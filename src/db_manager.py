import pymongo
import pandas as pd
from registro import Registro

csvFile = "Data/Monitoring report.csv"

class MongoDBManager:
    def __init__(self, connection_string, database_name, collection_name):
        self.client = pymongo.MongoClient(connection_string)
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]
        self.collection.create_index("Date", unique=True)  # Crear índice en el campo "Date"

    def init_data(self):
        df_csv = pd.read_csv(csvFile)
        registros_csv = [Registro.from_dict(row.to_dict()) for _, row in df_csv.iterrows()]
        existing_dates = set(self.collection.distinct("Date"))
        new_records = []
        for registro in registros_csv:
            registro_dict = registro.dict()
            if registro_dict["Date"] not in existing_dates:
                new_records.append(registro_dict)

        if new_records:
            self.insert_data(new_records)

    def insert_data(self, data_dict):
        self.collection.insert_one(data_dict)

    def get_data(self):
        data = list(self.collection.find())
        return pd.DataFrame(data)

    def update_data_from_csv(self):
        self.init_data()