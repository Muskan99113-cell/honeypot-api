from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import re

app = FastAPI()

API_KEY = "mysecurekey123"

# Request Body Model
class MessageRequest(BaseModel):
    sessionId: str
    message: str


@app.get("/")
def root():
    return {"message": "Muskan, Tejasvi, Taniya"}


# Function to extract scam intelligence
def extract_intelligence(text):

    upi_ids = re.findall(r'\b[\w.-]+@[\w.-]+\b', text)
    phone_numbers = re.findall(r'\b\d{10}\b', text)
    links = re.findall(r'https?://\S+', text)

    return {
        "upiIds": upi_ids,
        "phoneNumbers": phone_numbers,
        "phishingLinks": links
    }


@app.post("/honeypot")
def honeypot(request: MessageRequest, api_key: str = Header(None)):

    # API Key Check
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")

    text = request.message.lower()

    scam_keywords = ["otp", "bank", "upi", "verify", "urgent"]

    scam_detected = any(word in text for word in scam_keywords)

    intelligence = extract_intelligence(request.message)

    return {
        "sessionId": request.sessionId,
        "scam_detected": scam_detected,
        "received_message": request.message,
        "extracted_intelligence": intelligence
    }
