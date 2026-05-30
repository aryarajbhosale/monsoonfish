from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

from routes.process import router as process_router

app = FastAPI(
    title="Logo Processing Service",
    description="Upload a logo and receive silhouette, border, and grayscale versions via email.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

OUTPUTS_DIR = Path("outputs")
OUTPUTS_DIR.mkdir(exist_ok=True)

app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(process_router, prefix="/api")


@app.get("/", response_class=HTMLResponse)
async def index():
    html_path = Path("static/index.html")
    return FileResponse(str(html_path))
