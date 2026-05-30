from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pathlib import Path

from services.image_processor import process_image
from services.email_service import send_processed_images
from utils.validators import validate_upload

router = APIRouter()

OUTPUTS_DIR = Path("outputs")


@router.post("/process")
async def process_logo(file: UploadFile = File(...)):
    file_bytes = await file.read()

    validate_upload(file, file_bytes)

    try:
        file_paths = process_image(file_bytes, OUTPUTS_DIR)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Image processing failed: {str(exc)}",
        )

    email_status = "sent"
    try:
        send_processed_images(file_paths)
    except EnvironmentError as exc:
        email_status = f"failed: {str(exc)}"
    except FileNotFoundError as exc:
        email_status = f"failed: {str(exc)}"
    except Exception as exc:
        email_status = f"failed: {str(exc)}"

    return JSONResponse(
        content={
            "silhouette": "generated",
            "border": "generated",
            "grayscale": "generated",
            "email_status": email_status,
        }
    )
