from pydantic import BaseModel
from datetime import date

class EquipmentCreate(BaseModel):
    name: str
    brose_sap: str
    serial_number: str
    location: str
    responsible_person: str
    last_calibration: date
    interval_days: int
    calibration_location: str
    calibration_provider: str
    calibration_price: float
