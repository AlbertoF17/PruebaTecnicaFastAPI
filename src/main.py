from fastapi import FastAPI, Path, HTTPException
from typing import List
from utils import leer_csv
from registro import Registro
import db_manager
import plotly.graph_objs as go
from plotly.subplots import make_subplots


app = FastAPI()

@app.get("/registros")
def obtener_registros():
    registros = leer_csv("Data/Monitoring report.csv")
    return registros


@app.get("/registros/{num}")
def obtener_registro(num: int = Path(..., title="Número del registro")):
    registros = obtener_registros()
    if num < 0 or num >= len(registros):
        return {"error": "No existe este registro"}
    return registros[num]


@app.post("/registros")
def agregar_registro(registro: Registro):
    if not registro.validate(Registro):
        raise HTTPException(status_code=400, detail="Los datos del registro no son válidos")
    else:
        registros = obtener_registros()
        registros.append(registro)
        db_manager.insert_data(registro.dict())
    return {"mensaje": "Registro agregado exitosamente"}

@app.get("/grafico")
def obtener_grafico():
    registros = obtener_registros

    fig = go.Figure()
    for registro in registros:
        fig.add_trace(go.Scatter(x=[registro.Date], y=[registro.Energy_kWh], mode="lines+markers", name="Energy (kWh)"))

    fig.update_layout(title="Consumo de Energía",
                      xaxis_title="Fecha",
                      yaxis_title="Energía (kWh)")

    return fig

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
