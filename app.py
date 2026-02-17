"""
FastAPI backend for AI Fake Review Detector.
New review check endpoint calls Gemini AI agent.
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict
from dotenv import load_dotenv
import google.generativeai as genai

from agent import analyze_review

load_dotenv()

app = FastAPI()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


# CORS: allow Vite dev server (any port)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all (needed for extension)
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)



class CheckReviewRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")

    review_text: str = ""
    review_source: str = ""
    stay_date: str = ""
    stay_type: str = ""
    stars: int | None = None


class CheckReviewResponse(BaseModel):
    is_fake: bool
    genuine_score: float
    fake_score: float
    reason: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/check-review", response_model=CheckReviewResponse)
def check_review(body: CheckReviewRequest):
    """
    Expects: review_text, review_source, stay_date, stay_type, stars (optional 1-5).
    Returns: is_fake, genuine_score, fake_score, reason.
    """
    try:
        review_text = (body.review_text or "").strip()
        review_source = (body.review_source or "").strip()
        stay_date = (body.stay_date or "").strip()
        stay_type = (body.stay_type or "").strip()
        stars = body.stars
        if stars is not None and (stars < 1 or stars > 5):
            stars = None

        result = analyze_review(
            review_text=review_text,
            review_source=review_source,
            stay_date=stay_date,
            stay_type=stay_type,
            stars=stars,
        )
        return result
    except Exception as e:
        return CheckReviewResponse(
            is_fake=False,
            genuine_score=70.0,
            fake_score=30.0,
            reason=f"Server error: {str(e)}",
        )
