from fastapi import FastAPI, Header, HTTPException, Request
from pydantic import BaseModel
import re

app = FastAPI()

API_KEY = "mysecurekey123"

class MessageRequest(BaseModel):
    sessionId: str = "default"
    message: str = ""

@app.get("/")
def root():
    return {"status": "honeypot api live"}

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
async def honeypot(
    request: Request,
    x_api_key: str = Header(None)
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    try:
        body = await request.json()
    except:
        body = {}

    session_id = body.get("sessionId", "default")
    message = body.get("message", "")

    scam_keywords = ["otp", "bank", "upi", "verify", "urgent"]
    scam_detected = any(word in message.lower() for word in scam_keywords)

    intelligence = extract_intelligence(message)

    return {
        "sessionId": session_id,
        "scam_detected": scam_detected,
        "received_message": message,
        "extracted_intelligence": intelligence,
        "agentResponse": "Please hold while I verify your details."
    }
