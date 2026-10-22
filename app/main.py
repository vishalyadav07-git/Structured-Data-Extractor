from fastapi import FastAPI, HTTPException
from app.schemas import Validating
from google import genai
from dotenv import load_dotenv
import os
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
model = os.getenv("GEMINI_MODEL")

from app.extractor import call_gemini, process_response
app = FastAPI(title="Nestack Structured Data Extractor",
    description="Extract structured fields from unstructured text.",
    version="1.0.0",)


@app.post("/extract")
def extract(request: Validating):
    try:
        raw_response = call_gemini(
            client,
            model,
            request.text
        )

        result = process_response(raw_response)
        return result

    except ValueError:
        raise HTTPException(
            status_code=502,
            detail="The extraction service returned an invalid response."
        )

    