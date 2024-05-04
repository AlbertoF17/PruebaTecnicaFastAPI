from fastapi import FastAPI
import pandas as pd
from src.db_manager import MongoDBManager
from fastapi.templating import Jinja2Templates

connection_string = "mongodb+srv://albertofernandez:Alberto2002@energyconsumption.oayuede.mongodb.net/"
database_name = "EnergyConsumption"
collection_name = "consumption"
db_manager = MongoDBManager(connection_string, database_name, collection_name)


data = pd.read_csv("Data/Monitoring Report.csv")
data_dict = data.to_dict()

templates = Jinja2Templates(directory="templates")

app = FastAPI()

@app.get("/")
def get_index():
    return templates.TemplateResponse("index.html", context={"data_dict": data_dict})

@app.get("/datos/consumo")
def get_consumo():
    consumo_total = db_manager.get_total_consumption()
    return {"consumo_total": consumo_total + "kWh"}

@app.get("/datos/consumo/{fecha}")
def get_consumo_fecha(fecha: str):
    consumo_fecha = db_manager.get_consumption_by_date(fecha)
    return {"consumo_fecha": consumo_fecha + "kWh"}

@app.post("/save")
def set_registros(data):
    data_dict = data.to_dict(orient="records")
    db_manager.insert_data(data_dict)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)