from datetime import datetime
from pydantic import BaseModel, validator, root_validator, ValidationError
import math

class Registro(BaseModel):
    Date: str
    Energy_kWh: float
    Reactive_energy_kVArh: float
    Power_kW: float
    Maximeter_kW: float
    Reactive_power_kVAr: float
    Voltage_V: float
    Intensity_A: float
    Power_factor: float

    def __init__(self, **data):
        super().__init__(**data)
        for key, value in data.items():
            if isinstance(value, str) and value.lower() == 'nan':
                setattr(self, key, 0.0)
            elif isinstance(value, str) and value.replace('.', '', 1).isdigit():
                setattr(self, key, round(float(value), 3))

    def dict(self, *args, **kwargs):
        data = super().dict(*args, **kwargs)
        for key, value in data.items():
            if isinstance(value, float) and math.isnan(value):
                data[key] = None
        return data

    @classmethod
    def from_dict(cls, data):
        normalized_data = {
            "Date": data.get("Date"),
            "Energy_kWh": data.get("Energy (kWh)"),
            "Reactive_energy_kVArh": data.get("Reactive energy (kVArh)"),
            "Power_kW": data.get("Power (kW)"),
            "Maximeter_kW": data.get("Maximeter (kW)"),
            "Reactive_power_kVAr": data.get("Reactive power (kVAr)"),
            "Voltage_V": data.get("Voltage (V)"),
            "Intensity_A": data.get("Intensity (A)"),
            "Power_factor": data.get("Power factor (φ)")
        }
        return cls(**normalized_data)

    @validator('Date')
    def validar_date(cls, v):
        try:
            datetime.strptime(v, '%d %b %Y %H:%M:%S')
        except ValueError:
            raise ValueError("La fecha debe seguir el formato 'XX Mes(acortado) XXXX XX:XX:XX'")
        return v

    @root_validator
    def validar_floats(cls, values):
        for key, value in values.items():
            if key != 'Date':
                if isinstance(value, str) and not value.replace('.', '', 1).isdigit():
                    raise ValidationError(f"El campo '{key}' debe ser un número")
                elif isinstance(value, float):
                    values[key] = round(value, 3)
        return values