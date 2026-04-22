from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import joblib
import os
from feature_extraction import extract_features

app = FastAPI(
    title="CyberGuard URL Scanner API",
    description="API for detecting malicious URLs",
    version="1.0.0"
)

# Enable CORS for the browser extension to communicate with the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for the extension
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the trained model on startup
MODEL_PATH = "malicious_url_model.pkl"
model = None

@app.on_event("startup")
def load_model():
    global model
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
    else:
        print(f"Warning: Model file {MODEL_PATH} not found. Please train the model.")

class URLRequest(BaseModel):
    url: str

class ScanResult(BaseModel):
    url: str
    is_malicious: bool
    confidence: float
    features_analyzed: int

@app.get("/")
def read_root():
    return {"status": "CyberGuard API is running. Send POST requests to /scan endpoint."}

@app.post("/scan", response_model=ScanResult)
def scan_url(request: URLRequest):
    if not model:
        raise HTTPException(status_code=500, detail="Model is not loaded on the server.")
    
    url = request.url.strip()
    if not url:
        raise HTTPException(status_code=400, detail="Empty URL provided.")

    # Ensure URL has scheme
    if not url.startswith("http://") and not url.startswith("https://"):
        url_to_process = "http://" + url
    else:
        url_to_process = url

    try:
        # Extract features using existing logic
        features = extract_features(url_to_process)
        
        # Predict using the model
        features_df = pd.DataFrame([features])
        prediction = model.predict(features_df)[0]
        probability = model.predict_proba(features_df)[0]
        
        # Determine verdict
        is_malicious = bool(prediction == 1)
        confidence = float(probability[1] * 100) if is_malicious else float(probability[0] * 100)
        
        return ScanResult(
            url=url_to_process,
            is_malicious=is_malicious,
            confidence=confidence,
            features_analyzed=len(features)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing URL: {str(e)}")

# To run: uvicorn api:app --reload
