from fastapi import UploadFile, HTTPException

ALLOWED_CONTENT_TYPES = {"image/png", "image/jpeg", "image/jpg"}
ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg"}
MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB


def validate_upload(file: UploadFile, file_bytes: bytes) -> None:
    if file is None or file.filename == "":
        raise HTTPException(status_code=400, detail="No file provided or file is empty.")

    extension = _get_extension(file.filename)
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type '{extension}'. Allowed types: PNG, JPG, JPEG.",
        )

    content_type = (file.content_type or "").lower()
    if content_type and content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported content type '{content_type}'. Allowed: image/png, image/jpeg.",
        )

    if len(file_bytes) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    if len(file_bytes) > MAX_FILE_SIZE_BYTES:
        size_mb = len(file_bytes) / (1024 * 1024)
        raise HTTPException(
            status_code=413,
            detail=f"File size {size_mb:.2f} MB exceeds the maximum allowed size of 5 MB.",
        )


def _get_extension(filename: str) -> str:
    if not filename or "." not in filename:
        return ""
    return "." + filename.rsplit(".", 1)[-1].lower()
