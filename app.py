from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import spacy
import re
import uuid
import joblib

nlp = spacy.load("en_core_web_sm")

clf_pipeline = joblib.load("myenv/email_classifier_svm.pkl")

app = FastAPI()

class EmailRequest(BaseModel):
    email_text: str

REGEX_PATTERNS = {
    "EMAIL": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b',
    "PHONE": r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
    "CREDIT_CARD": r'(?:\d[ -]*?){13,16}',
    "IP": r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
}

def generate_token(label):
    return f"<{label}_{uuid.uuid4().hex[:6]}>"

def mask_pii(text):
    masked_text = text
    pii_map = {}

    for label, pattern in REGEX_PATTERNS.items():
        matches = re.findall(pattern, masked_text)
        for match in matches:
            token = generate_token(label)
            masked_text = masked_text.replace(match, token)
            pii_map[token] = match

    doc = nlp(masked_text)
    for ent in doc.ents:
        if ent.label_ in ["PERSON", "GPE", "ORG", "LOC", "DATE"]:
            if ent.text not in pii_map.values():
                token = generate_token(ent.label_)
                masked_text = masked_text.replace(ent.text, token)
                pii_map[token] = ent.text

    return masked_text, pii_map

def classify_email(masked_email):
    predicted_category = clf_pipeline.predict([masked_email])[0]
    return predicted_category

@app.post("/process_email/")
async def process_email(request: EmailRequest):
    try:
        raw_email = request.email_text
        masked_email, pii_map = mask_pii(raw_email)
        category = classify_email(masked_email)

        response = {
            "original_email": raw_email, 
            "masked_email": masked_email,
            "predicted_category": category,
            "pii_map": pii_map
        }

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
