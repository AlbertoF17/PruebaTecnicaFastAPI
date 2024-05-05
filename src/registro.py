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
    def validar_registro(cls, registro):
        try:
            cls(**registro.dict())
            return True
        except ValidationError:
            return False
            
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
            if key != 'Date':  # Evitar redondear el campo Date
                if isinstance(value, str) and not value.replace('.', '', 1).isdigit():
                    raise ValidationError(f"El campo '{key}' debe ser un número")
                elif isinstance(value, float):
                    values[key] = round(value, 3)
        return values