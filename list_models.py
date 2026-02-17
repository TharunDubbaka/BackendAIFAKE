"""Run this to see which Gemini models your API key can use: python list_models.py"""
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

print("Models that support generateContent:\n")
for m in genai.list_models():
    if "generateContent" in (m.supported_generation_methods or []):
        # Name can be "models/gemini-1.5-flash" - we use the part after "models/"
        name = m.name if m.name else ""
        short = name.replace("models/", "") if name.startswith("models/") else name
        print(f"  {short}  (full: {name})")
print("\nUse one of the short names as GEMINI_MODEL in .env")
