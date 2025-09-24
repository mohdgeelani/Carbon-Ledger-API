from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base
from sqlalchemy.orm import relationship

class Record(Base):
    __tablename__ = "records"

    id = Column(String, primary_key=True, index=True)
    project_name = Column(String, nullable=False)
    registry = Column(String, nullable=False)
    vintage = Column(Integer, nullable=False)
    quantity = Column(Float, nullable=False)
    serial_number = Column(String, nullable=False) 
    events = relationship("Event", back_populates="record")

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    record_id = Column(String, ForeignKey("records.id"))
    event_type = Column(String, nullable=False)  
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    record = relationship("Record", back_populates="events")