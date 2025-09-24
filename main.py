from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models
from models import Record, Event
import hashlib
from pydantic import BaseModel


app = FastAPI()
Base.metadata.create_all(bind=engine)

class RecordCreate(BaseModel):
    project_name: str
    registry: str
    vintage: int
    quantity: float
    serial_number: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# @app.get("/")
# def read_root():
#     return {"message": "Carbon Ledger API is running"}

@app.post("/records")
def create_record(record: RecordCreate, db: Session = Depends(get_db)):
   
    id_source = f"{record.project_name}:{record.registry}:{record.vintage}:{record.quantity}:{record.serial_number}"
    record_id = hashlib.sha256(id_source.encode()).hexdigest()

    db_record = db.query(Record).filter(Record.id == record_id).first()
    if db_record:
        raise HTTPException(status_code=400, detail="Record already exists")

    # Create new record
    new_record = Record(
        id=record_id,
        project_name=record.project_name,
        registry=record.registry,
        vintage=record.vintage,
        quantity=record.quantity,
        serial_number=record.serial_number
    )
    db.add(new_record)

    # Add "created" event
    event = Event(
        record_id=record_id,
        event_type="created"
    )
    db.add(event)

    db.commit()
    db.refresh(new_record)

    return {"id": record_id, "message": "Record created successfully"}


@app.post("/records/{record_id}/retire")
def retire_record(record_id: str, db: Session = Depends(get_db)):
    # Find the record by ID
    db_record = db.query(Record).filter(Record.id == record_id).first()
    if not db_record:
        raise HTTPException(status_code=404, detail="Record not found")

    # Check if it's already retired
    existing_retire_event = (
        db.query(Event)
        .filter(Event.record_id == record_id, Event.event_type == "retired")
        .first()
    )
    if existing_retire_event:
        raise HTTPException(status_code=400, detail="Record already retired")

    # Add "retired" event
    retire_event = Event(
        record_id=record_id,
        event_type="retired"
    )
    db.add(retire_event)
    db.commit()
    db.refresh(retire_event)

    return {"id": record_id, "message": "Record retired successfully"}

@app.get("/records/{record_id}")
def get_record(record_id: str, db: Session = Depends(get_db)):
    
    db_record = db.query(Record).filter(Record.id == record_id).first()
    if not db_record:
        raise HTTPException(status_code=404, detail="Record not found")

    events = db.query(Event).filter(Event.record_id == record_id).all()
    event_list = [{"type": e.event_type, "timestamp": e.timestamp} for e in events]

    return {
        "id": db_record.id,
        "project_name": db_record.project_name,
        "registry": db_record.registry,
        "vintage": db_record.vintage,
        "quantity": db_record.quantity,
        "serial_number": db_record.serial_number,
        "events": event_list
    }



