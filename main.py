from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from .database import SessionLocal, engine
from .models import Base, Applicant
from .security import fingerprint
from .config import MAX_USERS, DAYS_LIMIT, START_DATE

Base.metadata.create_all(bind=engine)

app = FastAPI(title="DAKCAMERA API")

# Allow frontend calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your domain in production
    allow_methods=["*"],
    allow_headers=["*"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/apply")
async def apply(request: Request):
    db: Session = next(get_db())
    data = await request.json()
    
    ip = request.client.host
    ua = request.headers.get("user-agent", "")
    device_id = fingerprint(ip, ua)

    total = db.query(Applicant).count()
    if total >= MAX_USERS:
        raise HTTPException(status_code=403, detail="Nafasi zimejaa")

    if datetime.utcnow() > START_DATE + timedelta(days=DAYS_LIMIT):
        raise HTTPException(status_code=403, detail="Muda umeisha")

    exists = db.query(Applicant).filter(
        (Applicant.ip_address == ip) | (Applicant.device_id == device_id)
    ).first()
    if exists:
        raise HTTPException(status_code=403, detail="Ombi tayari lipo")

    applicant = Applicant(
        full_name=data.get("name"),
        phone=data.get("phone"),
        age=data.get("age"),
        email=data.get("email"),
        ip_address=ip,
        device_id=device_id
    )

    db.add(applicant)
    db.commit()

    return {
        "status": "approved",
        "message": "Umefanikiwa kujiunga DakCamera Beta",
        "company": "CIPHER TECH",
        "project": "DAKCAMERA"
    }