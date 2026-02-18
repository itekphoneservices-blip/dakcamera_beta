from sqlalchemy import Column, Integer, String, DateTime
from .database import Base
from datetime import datetime

class Applicant(Base):
    __tablename__ = "applicants"

    id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)
    phone = Column(String, unique=True)
    age = Column(Integer, nullable=False)
    email = Column(String)
    ip_address = Column(String, unique=True)
    device_id = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)