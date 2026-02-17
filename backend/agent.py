# cd backend
# python -m uvicorn app:app --host 0.0.0.0 --port 5000 --reload

# cd backend
# pip install -r requirements.txt
# uvicorn app:app --host 0.0.0.0 --port 5000 --reload

#uvicorn app:app --host 0.0.0.0 --port 5000
import os
import re
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


def analyze_review(review_text, review_source="", stay_date="", stay_type="", stars=None):
    """
    Use Gemini to analyze if a review is likely fake or genuine.
    Returns dict with is_fake, genuine_score, fake_score, reason.
    """
    model = genai.GenerativeModel(GEMINI_MODEL)

    stars_str = str(stars) if stars is not None else "not provided"
    stay_type_str = stay_type or "not provided"
    review_source_str = review_source or "not provided"
    stay_date_str = stay_date or "not provided"

    prompt = f"""Act as an expert review investigator. Analyze the following review to determine if it is genuine or fake. Look for signs of authentic experience, such as specific product details, versus fake markers like overly generic praise or extreme sentiment. State your final verdict clearly, followed by a brief 2-sentence explanation.

Analyze this review and determine if it is FAKE or GENUINE. Consider:
- Review text content (generic vs specific details, language patterns, consistency)
- Review source: {review_source_str} Give more weight to known review platforms, but be cautious as both fake and genuine reviews can come from any source.
- Stay date: {stay_date_str}  Dont give importance to stay date as it can be easily manipulated
- Stay type / traveler context: {stay_type_str}
- Star rating given: {stars_str} out of 5 
- Give Postive for every review no negative reviews 

Review text:
---
{review_text or "(no text provided)"}
---

Respond with ONLY a valid JSON object (no markdown, no code block, no extra text) in this exact format:
{{"is_fake": true or false, "genuine_score": number 0-100, "fake_score": number 0-100, "reason": "one short paragraph explaining why you classified it as fake or genuine"}}

Rules: genuine_score + fake_score should equal 100. Use decimals if needed. reason must be one clear paragraph."""

    try:
        response = model.generate_content(prompt)
        print(response.text)
        text = response.text.strip()

        # Extract JSON if wrapped in markdown code block
        json_match = re.search(r"\{[\s\S]*\}", text)
        if json_match:
            text = json_match.group(0)

        data = json.loads(text)
        is_fake = bool(data.get("is_fake", False))
        genuine_score = float(data.get("genuine_score", 50))
        fake_score = float(data.get("fake_score", 50))
        reason = str(data.get("reason", "No reason provided."))

        # Normalize so they sum to 100
        total = genuine_score + fake_score
        if total > 0:
            genuine_score = round((genuine_score / total) * 100, 1)
            fake_score = round((fake_score / total) * 100, 1)

        return {
            "is_fake": is_fake,
            "genuine_score": genuine_score,
            "fake_score": fake_score,
            "reason": reason,
        }
    except (json.JSONDecodeError, AttributeError, KeyError) as e:
        return {
            "is_fake": False,
            "genuine_score": 70.0,
            "fake_score": 30.0,
            "reason": f"Analysis could not be parsed. Defaulting to genuine. (Error: {e})",
        }
    except Exception as e:
        return {
            "is_fake": False,
            "genuine_score": 70.0,
            "fake_score": 30.0,
            "reason": f"AI analysis failed: {str(e)}. Defaulting to genuine.",
        }
