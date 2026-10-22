
import os
from dotenv import load_dotenv
from google import genai
from app.extractor import process_response

from app.extractor import call_gemini

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
model = os.getenv("GEMINI_MODEL")

client = genai.Client(api_key=api_key)

text = """
Receipt from AWS India Pvt Ltd.
Total: INR 1250.
Date: 2024-03-12.
"""

result = call_gemini(client, model, text)

data = process_response(result)
for field in [
    "vendor_name",
    "amount",
    "currency",
    "date",
    "category",
    "description",
    "invoice_id",
]:
    print(field, ":", data["fields"][field]["value"])

print(type(data))
print("Review required:", data["review_required"])

print(result)

