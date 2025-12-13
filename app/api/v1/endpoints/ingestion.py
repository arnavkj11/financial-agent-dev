import os
import shutil
from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException, Depends
from app.services.pdf import process_document_task
from app.api.deps import get_current_user
from app.models.sql import User

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/ingest")
async def ingest_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """
    Upload a PDF document for ingestion.
    The processing functionality happens in the background.
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    # Save file to disk
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not save file: {e}")

    # Trigger Background Task
    background_tasks.add_task(process_document_task, file_path, current_user.id)

    return {
        "message": "File uploaded successfully. Processing started.",
        "filename": file.filename
    }
