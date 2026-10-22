import json
from google import genai

from app.prompts import EXTRACTION_PROMPT

from datetime import datetime

THRESHOLD = 0.75

FIELD_NAMES = [
    "vendor_name",
    "amount",
    "currency",
    "date",
    "category",
    "description",
    "invoice_id",
]

STRING_FIELDS = [
    "vendor_name",
    "currency",
    "date",
    "category",
    "description",
    "invoice_id",
]

def normalize_value(field_name, value):
    if value is None:
        return None
    
    if not isinstance(value, str) and field_name != "amount":
        return None

    if field_name == "amount":
        try:
            amount = float(value)

            if amount < 0:
                return None

            if amount.is_integer():
                return int(amount)

            return amount

        except (ValueError, TypeError):
            return None
        
    if field_name == "currency":
        return value.strip().upper()

    if field_name == "category":
        value = value.strip().lower()
        if value not in {"food", "travel", "utilities", "software", "other"}:
            return None
        return value


    if field_name == "date":
        for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y"):
            try:
                return datetime.strptime(value.strip(), fmt).date().isoformat()
            
            except ValueError:
                continue
        return None

    
    return value

# print(normalize_value("amount", "1250"))
# print(normalize_value("amount", "1250.50"))
# print(normalize_value("amount", "unknown"))
# print(normalize_value("amount", None))
# print(normalize_value("currency", " inr "))
# print(normalize_value("category", "SOFTWARE"))
# print(normalize_value("category", "entertainment"))
# print(normalize_value("date", "2024-04-29"))
# print(normalize_value("date", "29-04-2024"))
# print(normalize_value("date", "29/04/2024"))
# print(normalize_value("date", "not a date"))
# print(normalize_value("currency", 123))
# print(normalize_value("category", "SOFTWARE"))
# print(normalize_value("date", "29-04-2024"))


def call_gemini(client, model, text):
    prompt = EXTRACTION_PROMPT.replace("{text}",text)
    

    response = client.models.generate_content(
        model=model,
        contents=prompt,
    )

    return response.text

def process_response(raw_response):
    data = json.loads(raw_response)
    processed_fields = {}
    for name in FIELD_NAMES:
        item = data[name]
        value = normalize_value(name,item["value"])
        # print("DEBUG:", name, repr(item["value"]), "->", repr(value))
        confidence = item["confidence"]
        needs_review = (confidence < THRESHOLD or value is None)
        processed_fields[name] = {
            "value": value,
            "confidence": confidence,
            "needs_review": needs_review,
            }
    review_required = any(item["needs_review"] for item in processed_fields.values())
    return {
    "review_required": review_required,
    "fields": processed_fields,
    }
