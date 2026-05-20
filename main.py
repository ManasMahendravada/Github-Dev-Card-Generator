"""
GitHub Dev Card Generator — FastAPI Backend
"""
# load_dotenv MUST be called before any local module imports
import os
from dotenv import load_dotenv
load_dotenv()

import logging
import re
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from github_api import fetch_github_profile
from gemini_api import analyze_github_profile
from card_generator import generate_card_html, save_card

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s — %(message)s",
)
logger = logging.getLogger("main")

BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / "static"
CARDS_DIR = STATIC_DIR / "cards"
CARDS_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="GitHub Dev Card Generator", version="2.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


def extract_username(raw: str) -> str:
    """Accepts username, @username, or full github.com URL."""
    raw = raw.strip()
    url_match = re.search(r"github\.com/([A-Za-z0-9_.\-]+)", raw)
    if url_match:
        return url_match.group(1).strip("/")
    return raw.lstrip("@").strip("/")


class GenerateRequest(BaseModel):
    username: str


@app.get("/health")
async def health():
    return {"status": "ok", "version": "2.1.0"}


@app.get("/")
async def root():
    return {"message": "GitHub Dev Card Generator API is running!", "docs": "/docs"}


@app.post("/generate")
async def generate_card(request: GenerateRequest):
    username = extract_username(request.username)
    if not username:
        raise HTTPException(status_code=400, detail="Username cannot be empty.")

    logger.info(f"[START] Input='{request.username}' → Username='{username}'")

    try:
        github_data = await fetch_github_profile(username)
        logger.info(f"[GITHUB] {github_data['name']} | repos={github_data['public_repos']}")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"GitHub API error: {e}")

    try:
        analysis = await analyze_github_profile(github_data)
    except Exception as e:
        logger.warning(f"[GEMINI] Failed ({e}), using fallback")
        from gemini_api import _fallback_analysis
        analysis = _fallback_analysis(github_data)

    card_html = generate_card_html(username, github_data, analysis)
    card_url = save_card(username, card_html, BASE_DIR)
    logger.info(f"[DONE] Saved → {card_url}")

    return {
        "status": "success",
        "username": username,
        "card_url": card_url,
        "card_html": card_html,
        "github_data": github_data,
        "analysis": analysis,
        "message": f"Dev card generated for {github_data['name']}",
    }


@app.get("/card/{username}")
async def get_card(username: str):
    file_path = CARDS_DIR / f"{username}.html"
    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"No card for '{username}'. Generate first.")
    return FileResponse(str(file_path), media_type="text/html")


@app.get("/api/github/{username}")
async def get_github_raw(username: str):
    try:
        return await fetch_github_profile(username)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8080)), reload=True)
