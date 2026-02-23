from fastapi import FastAPI
from .database import engine, Base
from .routes import equipment

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Calibration Tracker")

app.include_router(equipment.router)