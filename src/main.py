from fastapi import FastAPI, Path, HTTPException, Response
from fastapi.responses import HTMLResponse
from typing import List
from utils import leer_csv, escribir_en_csv
from registro import Registro
from db_manager import MongoDBManager
import plotly.graph_objs as go
import pandas as pd

csv = "Data/Monitoring report.csv"
db_manager = MongoDBManager("mongodb+srv://albertofernandez:Alberto2002@energyconsumption.oayuede.mongodb.net/", "EnergyConsumption", "consumption")
db_manager.init_data()
with open("index.html", "r") as file:
    html_content = file.read()

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
async def agregar_registro(registro: Registro):
    escribir_en_csv(registro.dict(), csv)
    registros_dict = [registro.dict() for registro in obtener_registros()]
    db_manager.insert_data(registros_dict)
    return {"mensaje": "Registro agregado exitosamente"}


@app.get("/", response_class=HTMLResponse)
async def read_root():
    return html_content


@app.get("/graphs/{graph}")
async def generate_graph(graph: str, response: Response):
    df = pd.read_csv(csv)
    df['Date'] = pd.to_datetime(df['Date'])

    graph_operations = {
        "energy": ("Energy (kWh)", "Consumo de Energía"),
        "reactive energy": ("Reactive energy (kVArh)", "Energía Reactiva"),
        "power": ("Power (kW)", "Potencia"),
        "maximeter": ("Maximeter (kW)", "Maxímetro"),
        "reactive power": ("Reactive power (kVAr)", "Potencia Reactiva"),
        "voltage": ("Voltage (V)", "Voltaje"),
        "intensity": ("Intensity (A)", "Intensidad"),
        "power factor": ("Power factor (φ)", "Factor Potencial")
    }

    if graph not in graph_operations:
        raise HTTPException(status_code=404, detail="Graph not found")

    consumo_por_fecha = df.groupby(df['Date'].dt.strftime('%Y-%m-%d'))[graph_operations[graph][0]].sum().reset_index()
    consumo_por_fecha['Date'] = pd.to_datetime(consumo_por_fecha['Date'], format='%Y-%m-%d').dt.strftime('%Y-%m-%d')
    consumo_por_fecha = consumo_por_fecha.sort_values(by='Date')

    fig = go.Figure()
    fig.add_trace(go.Bar(x=consumo_por_fecha['Date'], y=consumo_por_fecha[graph_operations[graph][0]], name=graph_operations[graph][1]))
    fig.update_layout(title=graph_operations[graph][1], xaxis_title="Fecha", yaxis_title=f"{graph_operations[graph][1]} ({graph_operations[graph][0]})")
    fig.update_xaxes(tickformat="%d-%m-%Y")
    
    fig_json = fig.to_json()
    return fig_json


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
