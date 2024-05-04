import pandas as pd
from registro import Registro

def leer_csv(nombre_archivo):
    df = pd.read_csv("Data/Monitoring report.csv")
    
    mapeo_nombres = {
        'Date': 'Date',
        'Energy (kWh)': 'Energy_kWh',
        'Reactive energy (kVArh)': 'Reactive_energy_kVArh',
        'Power (kW)': 'Power_kW',
        'Maximeter (kW)': 'Maximeter_kW',
        'Reactive power (kVAr)': 'Reactive_power_kVAr',
        'Voltage (V)': 'Voltage_V',
        'Intensity (A)': 'Intensity_A',
        'Power factor (φ)': 'Power_factor'
    }
    
    df.rename(columns=mapeo_nombres, inplace=True)
    
    registros_dict = df.to_dict(orient='records')

    lista_registros = []
    for registro in registros_dict:
        registro_obj = Registro(**registro)
        lista_registros.append(registro_obj)  
    
    return lista_registros