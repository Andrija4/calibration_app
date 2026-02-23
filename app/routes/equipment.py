from fastapi import APIRouter, Depends, Request, Form, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from datetime import date
import asyncio
import json

from ..database import SessionLocal
from .. import crud, schemas

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                pass

manager = ConnectionManager()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def read_equipment(request: Request, db: Session = Depends(get_db)):
    '''
    Retrieve all equipment entries from the database and render the index page with the equipment list.
    '''
    equpiment = crud.get_all_equipment(db)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "equipment": equpiment}
    )

@router.get("/create")
def create_form(request: Request):
    return templates.TemplateResponse("create_equipment.html", {"request": request})

@router.post("/create")
def create_equipment(
    name: str = Form(...),
    brose_sap: str = Form(...),
    serial_number: str = Form(...),
    location: str = Form(...),
    responsible_person: str = Form(None),
    last_calibration: date = Form(...),
    interval_days: int = Form(...),
    calibration_location: str = Form(None),
    calibration_provider: str = Form(None),
    calibration_price: float = Form(None),
    db: Session = Depends(get_db)
):
    '''
    Create a new equipment entry based on form input and save to the database.
    '''
    equipment_data = schemas.EquipmentCreate(
        name=name,
        brose_sap=brose_sap,
        serial_number=serial_number,
        location=location,
        responsible_person=responsible_person,
        last_calibration=last_calibration,
        interval_days=interval_days,
        calibration_location=calibration_location,
        calibration_provider=calibration_provider,
        calibration_price=calibration_price
    )
    crud.create_equipment(db, equipment_data)
    return RedirectResponse(url="/", status_code=303)

@router.post("/calibrate/{equipment_id}")
def calibrate(equipment_id: int, db: Session = Depends(get_db)):
    '''
    Trigger calibration for the specified equipment and update its status in the database.
    '''
    crud.calibrate_equipment(db, equipment_id)
    return RedirectResponse(url="/", status_code=303)

@router.post("/delete/{equipment_id}")
def delete_equipment(equipment_id: int, db: Session = Depends(get_db)):
    equipment = db.query(crud.models.Equipment).filter(crud.models.Equipment.id == equipment_id).first()
    if equipment:
        db.delete(equipment)
        db.commit()
    return RedirectResponse(url="/", status_code=303)

@router.get("/edit/{equipment_id}")
def edit_form(request: Request, equipment_id: int, db: Session = Depends(get_db)):
    '''
    Render the edit form for a specific equipment entry. If the equipment does not exist, redirect to the index page.
    '''
    equipment = db.query(crud.models.Equipment).filter(crud.models.Equipment.id == equipment_id).first()
    if not equipment:
        return RedirectResponse(url="/", status_code=303)
    return templates.TemplateResponse("edit_equipment.html", {"request": request, "equipment": equipment})

@router.post("/update/{equipment_id}")
def update_equipment(
    equipment_id: int,
    name: str = Form(...),
    brose_sap: str = Form(...),
    serial_number: str = Form(...),
    location: str = Form(...),
    responsible_person: str = Form(None),
    last_calibration: date = Form(...),
    interval_days: int = Form(...),
    calibration_location: str = Form(None),
    calibration_provider: str = Form(None),
    calibration_price: float = Form(None),
    db: Session = Depends(get_db)
):
    '''
    Update equipment details based on form input and save to the database.
    '''
    equipment_data = schemas.EquipmentCreate(
        name=name,
        brose_sap=brose_sap,
        serial_number=serial_number,
        location=location,
        responsible_person=responsible_person,
        last_calibration=last_calibration,
        interval_days=interval_days,
        calibration_location=calibration_location,
        calibration_provider=calibration_provider,
        calibration_price=calibration_price
    )
    crud.update_equipment(db, equipment_id, equipment_data)
    return RedirectResponse(url="/", status_code=303)

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    '''
    WebSocket endpoint to send real-time status updates to clients.
    '''
    await manager.connect(websocket)
    try:
        while True:
            # Send status update every 5 seconds
            await asyncio.sleep(5)
            db = SessionLocal()
            equipment_list = crud.get_all_equipment(db)
            db.close()
            
            status_data = []
            for eq in equipment_list:
                status_data.append({
                    "id": eq.id,
                    "status": eq.status,
                    "next_calibration": str(eq.next_calibration)
                })
            
            await manager.broadcast(json.dumps(status_data))
    except WebSocketDisconnect:
        manager.disconnect(websocket)