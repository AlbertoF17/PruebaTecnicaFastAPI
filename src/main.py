from fastapi import FastAPI, Path, HTTPException
from typing import List
from utils import leer_csv, escribir_en_csv
from registro import Registro
from db_manager import MongoDBManager
import plotly.graph_objs as go
import pandas as pd
from plotly.subplots import make_subplots

csv = "Data/Monitoring report.csv"
db_manager = MongoDBManager("mongodb+srv://albertofernandez:Alberto2002@energyconsumption.oayuede.mongodb.net/", "EnergyConsumption", "consumption")
db_manager.init_data()

app = FastAPI()

@app.get("/registros")
def obtener_registros():
    registros = leer_csv(csv)
    return registros


@app.get("/registros/{num}")
def obtener_registro(num: int = Path(..., title="Número del registro")):
    registros = obtener_registros()
    if num < 0 or num >= len(registros):
        return {"error": "No existe este registro"}
    return registros[num]


@app.post("/registros")
def agregar_registro(registro: Registro):
    if not Registro.validar_registro(registro):
        raise HTTPException(status_code=400, detail="Los datos del registro no son válidos")
    else:
        escribir_en_csv(registro.dict(), csv)
        registros_dict = [registro.dict() for registro in obtener_registros()]
        db_manager.insert_data(registros_dict)
    return {"mensaje": "Registro agregado exitosamente"}


@app.get("/grafico")
def obtener_grafico():
    df_first_row = pd.read_csv(csv, header=0, nrows=1)
    column_names = df_first_row.columns.tolist()
    df = pd.read_csv(csv, names=column_names)

    consumo_por_fecha = df.groupby('Date')['Energy (kWh)'].sum().reset_index()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=consumo_por_fecha['Date'], y=consumo_por_fecha['Energy (kWh)'], mode="lines+markers", name="Consumo de energía"))

    fig.update_layout(title="Consumo de Energía",
                      xaxis_title="Fecha",
                      yaxis_title="Energía (kWh)")
    return fig

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
