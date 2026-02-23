from sqlalchemy.orm import Session
from . import models, schemas
from datetime import date

def get_all_equipment(db: Session):
    return db.query(models.Equipment).all()

def create_equipment(db: Session, equipment: schemas.EquipmentCreate):
    '''
    Create a new equipment entry in the database based on the provided equipment data.
    '''
    db_equipment = models.Equipment(**equipment.dict())
    db.add(db_equipment)
    db.commit()
    db.refresh(db_equipment)
    return db_equipment

def calibrate_equipment(db: Session, equipment_id: int):
    '''
    Calibrate the specified equipment by updating its last_calibration date to today and recalculating the next calibration date.
    '''
    equipment = db.query(models.Equipment).filter(models.Equipment.id == equipment_id).first()
    if equipment:
        equipment.last_calibration = date.today()
        db.commit()
        db.refresh(equipment)
    return equipment

def update_equipment(db: Session, equipment_id: int, equipment_data: schemas.EquipmentCreate):
    '''
    Update an existing equipment entry in the database with new data provided in the equipment_data object.
    '''
    equipment = db.query(models.Equipment).filter(models.Equipment.id == equipment_id).first()
    if equipment:
        for key, value in equipment_data.dict().items():
            setattr(equipment, key, value)
        db.commit()
        db.refresh(equipment)
    return equipment