import pandas as pd
import csv
from registro import Registro

csvFile = "Data/Monitoring report.csv"

def leer_csv(nombre_archivo):
    df = pd.read_csv(csvFile)
    
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

def escribir_en_csv(registro_dict, csvFile):
    with open(csvFile, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=registro_dict.keys())
        if file.tell() == 0:
            writer.writeheader()

        writer.writerow(registro_dict)