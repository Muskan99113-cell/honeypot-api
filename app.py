from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import re
import random

app = FastAPI()

API_KEY = "mysecurekey123"


# ------------------------------
# Request Model (tester-safe)
# ------------------------------
class MessageRequest(BaseModel):
    sessionId: str = "auto"
    message: str = "test"
    history: list[str] = []


# ------------------------------
# Health Endpoints
# ------------------------------
@app.get("/")
def root():
    return {"status": "API live"}


@app.get("/health")
def health():
    return {"status": "alive"}


# ------------------------------
# Scam Detection Logic
# ------------------------------
def detect_scam(text):
    text = text.lower()

    risk_patterns = [
        "otp", "bank", "upi", "verify", "urgent",
        "account blocked", "kyc", "refund",
        "click link", "limited time"
    ]

    score = sum(1 for word in risk_patterns if word in text)

    return score >= 2, score


# ------------------------------
# Intelligence Extraction
# ------------------------------
def extract_intelligence(text):
    upi_ids = re.findall(r'\b[\w.-]+@[\w.-]+\b', text)
    phone_numbers = re.findall(r'\b\d{10}\b', text)
    links = re.findall(r'https?://\S+', text)

    return {
        "upiIds": upi_ids,
        "phoneNumbers": phone_numbers,
        "phishingLinks": links
    }


# ------------------------------
# Agent Response Generator
# ------------------------------
def agent_reply():
    replies = [
        "Okay sir, I am checking your request now.",
        "Please hold on while I verify your details.",
        "Let me confirm this from the system.",
        "Processing… one moment please."
    ]
    return random.choice(replies)


# ------------------------------
# Honeypot Endpoint
# ------------------------------
@app.post("/honeypot")
def honeypot(request: MessageRequest, api_key: str = Header(None, alias="x-api-key")):

    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    scam_detected, risk_score = detect_scam(request.message)
    intelligence = extract_intelligence(request.message)
    confidence = min(100, risk_score * 25)

    return {
        "sessionId": request.sessionId,
        "scamDetected": scam_detected,
        "riskScore": risk_score,
        "confidenceScore": confidence,
        "conversationTurns": len(request.history) + 1,
        "extractedIntelligence": intelligence,
        "agentResponse": agent_reply()
    }
