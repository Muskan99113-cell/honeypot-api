from fastapi import FastAPI, Header, HTTPException, Request
import re

app = FastAPI()

API_KEY = "mysecurekey123"


@app.get("/")
def root():
    return {"status": "honeypot running"}


def extract_intelligence(text: str):
    upi_ids = re.findall(r'\b[\w.-]+@[\w.-]+\b', text)
    phone_numbers = re.findall(r'\b\d{10}\b', text)
    links = re.findall(r'https?://\S+', text)

    return {
        "upiIds": upi_ids,
        "phoneNumbers": phone_numbers,
        "phishingLinks": links
    }


@app.post("/honeypot")
async def honeypot(request: Request, x_api_key: str = Header(None)):

    # Authentication
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    # Accept ANY body safely
    try:
        body = await request.json()
    except:
        body = {}

    # Extract message from multiple possible tester formats
    message = ""

    if isinstance(body, dict):
        message = (
            body.get("message")
            or body.get("text")
            or body.get("content")
            or body.get("input")
            or ""
        )

    message = str(message)

    scam_keywords = ["otp", "bank", "upi", "verify", "urgent", "account", "payment"]
    scam_detected = any(word in message.lower() for word in scam_keywords)

    intelligence = extract_intelligence(message)

    return {
        "status": "processed",
        "scam_detected": scam_detected,
        "conversation_turns": 1,
        "engagement_score": 1,
        "extracted_intelligence": intelligence,
        "agent_response": "Please hold while I verify your details."
    }
