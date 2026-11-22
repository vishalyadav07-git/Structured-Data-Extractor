# Structured Data Extractor

A Python-based structured data extraction API built with FastAPI and Google Gemini. It extracts transaction information from unstructured text, such as receipts, invoices, emails, and messages, and returns normalized JSON with per-field confidence scores and human-review flags.

## Live Deployment

**API Documentation (Swagger UI):** https://nestack-sde-0zjg.onrender.com/docs

**Endpoint:** `POST /extract`


## Features

- Extracts seven fields: vendor name, amount, currency, date, category, description, and invoice ID.
- Uses Google Gemini for LLM-based information extraction.
- Normalizes dates to `YYYY-MM-DD`.
- Normalizes currency codes and transaction amounts.
- Supports the categories `food`, `travel`, `utilities`, `software`, and `other`.
- Assigns a confidence score and `needs_review` flag to each field.
- Sets `review_required` when any field requires review.
- Provides a REST API using FastAPI and interactive documentation through Swagger UI.

## Tech Stack

- Python
- FastAPI
- Google Gemini API (`google-genai`)
- Pydantic
- python-dotenv
- Uvicorn

## Project Structure

```text
nestack_sde/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── extractor.py
│   ├── prompts.py
│   └── schemas.py
├── .env
├── .gitignore
├── test_gemini.py
└── README.md
```

## Setup and Installation

### 1. Clone the repository

```bash
git clone <YOUR_PRIVATE_REPOSITORY_URL>
cd nestack_sde
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install "fastapi[standard]" google-genai python-dotenv
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=your_supported_gemini_model
```

Replace the example values with your own credentials and configured model.

**Security:** Never commit your `.env` file or expose your Gemini API key.

### 5. Run the application

From the project root, run:

```bash
python -m uvicorn app.main:app --reload
```

The API will be available at:

- API root: http://127.0.0.1:8000/
- Swagger documentation: http://127.0.0.1:8000/docs

## API Usage

### POST `/extract`

Extracts structured transaction data from the supplied text.

#### Request

```json
{
  "text": "AWS India Pvt Ltd. Invoice INV-2024-0312. Date: 2024-03-12. Total: INR 1250 for cloud computing services."
}
```

#### Example response

```json
{
  "review_required": false,
  "fields": {
    "vendor_name": {
      "value": "AWS India Pvt Ltd",
      "confidence": 1.0,
      "needs_review": false
    },
    "amount": {
      "value": 1250,
      "confidence": 1.0,
      "needs_review": false
    },
    "currency": {
      "value": "INR",
      "confidence": 1.0,
      "needs_review": false
    },
    "date": {
      "value": "2024-03-12",
      "confidence": 1.0,
      "needs_review": false
    },
    "category": {
      "value": "software",
      "confidence": 0.9,
      "needs_review": false
    },
    "description": {
      "value": "Cloud computing services",
      "confidence": 1.0,
      "needs_review": false
    },
    "invoice_id": {
      "value": "INV-2024-0312",
      "confidence": 1.0,
      "needs_review": false
    }
  }
}
```

Confidence values in this example are illustrative; actual values may vary between model responses.

## Review Logic

The configured confidence threshold is `0.75`.

A field is marked for review when its confidence is below the threshold or its normalized value is `null`.

The top-level `review_required` flag is `true` if any field has `needs_review: true`.

For unrelated input, the intended behavior is to return all seven fields with `null` values, low confidence scores, and review flags enabled.

## Testing

Run the current Gemini integration test with:

```bash
python test_gemini.py
```

Use Swagger UI at `/docs` to test the `/extract` endpoint with receipts, emails, and unrelated text.

## Limitations

- Confidence scores are model-generated estimates and are not independently calibrated probabilities.
- Extraction quality depends on the supplied text and the model response.
- Additional validation and testing are needed to ensure robustness against malformed or incomplete model responses.
- No production deployment is configured by this README.

## License

Add the appropriate license information if the project is to be distributed publicly.
