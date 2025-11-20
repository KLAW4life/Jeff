from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request
from starlette.responses import JSONResponse

from server.config import Config
from server.models import JournalEntry, Patient, User
from server.routers.auth import login_required

router = APIRouter(prefix=Config.API_PREFIX)


@router.get("/patients/{patient_id}/entries")
async def list_entries(patient_id: str):
    patient = Patient.objects(id=patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    entries = []
    for e in patient.journal_entries:
        entries.append({
            "id": str(getattr(e, 'id', '')),
            "date": e.date,
            "location": e.location,
            "title": e.title,
            "message": e.message,
            "image_url": e.image_url,
            "emotion": e.emotion,
            "ai_response": e.ai_response,
        })

    return {"entries": entries}


@router.post("/patients/{patient_id}/entries")
async def add_entry(patient_id: str, request: Request, session=Depends(login_required)):
    payload = await request.json()
    patient = Patient.objects(id=patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    je = JournalEntry(
        date=payload.get("date", datetime.utcnow()),
        location=payload.get("location"),
        title=payload.get("title"),
        message=payload.get("message"),
        image_url=payload.get("image_url"),
        emotion=payload.get("emotion"),
        ai_response=payload.get("ai_response"),
    )

    patient.journal_entries.append(je)
    patient.save()

    return JSONResponse({"message": "Entry added"}, status_code=201)
