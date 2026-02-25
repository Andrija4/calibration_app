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
        # Reset flag so email can be sent again if needed
        equipment.email_sent_30_days = False
        equipment.email_sent_7_days = False
        equipment.email_sent_expired = False

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
        # Reset email_sent flag if last_calibration is being updated
        if 'last_calibration' in equipment_data.dict():
            equipment.email_sent_30_days = False
            equipment.email_sent_7_days = False
            equipment.email_sent_expired = False
        db.commit()
        db.refresh(equipment)
    return equipment

def get_all_mail(db: Session):
    return db.query(models.Mail).all()

def create_mail(db: Session, mail: schemas.MailCreate):
    '''
    Create a new mail entry in the database based on the provided mail data.
    '''
    db_mail = models.Mail(**mail.dict())
    db.add(db_mail)
    db.commit()
    db.refresh(db_mail)
    return db_mail