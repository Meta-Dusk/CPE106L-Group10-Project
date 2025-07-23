# api_test.py or main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext
from pymongo import MongoClient
from dotenv import load_dotenv
import os, requests
from pathlib import Path

# Import our API configuration service
from app.services.api_config import load_api_key, is_api_configured

load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".." / ".env")
# === MongoDB Setup ===
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client["chaewon_db"]
users_collection = db["users"]

# === Google Maps API Key ===
# Try to load from our secure configuration first, then fall back to environment
GOOGLE_MAPS_API_KEY = load_api_key() or os.getenv("GOOGLE_MAPS_API_KEY")

print("API KEY Source:", "App Configuration" if load_api_key() else "Environment Variable")
print("API KEY:", GOOGLE_MAPS_API_KEY[:10] + "..." if GOOGLE_MAPS_API_KEY and len(GOOGLE_MAPS_API_KEY) > 10 else "Not configured")

if not GOOGLE_MAPS_API_KEY:
    print("⚠️  Warning: No Google Maps API key configured. Please configure it in the app or set GOOGLE_MAPS_API_KEY in .env")
    # Don't raise error here - let the app start but handle missing key in route endpoints

# === Password Hashing ===
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash_password(pw): return pwd_context.hash(pw)
def verify_password(pw, hashed): return pwd_context.verify(pw, hashed)

# === FastAPI App ===
app = FastAPI(title="Chaewon Meet & Greet API", version="1.0.0")

# === Pydantic Models ===
class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    password: str
    confirm_password: str

class RouteRequest(BaseModel):
    origin: str
    destination: str

class RideRequest(BaseModel):
    user_id: str
    pickup: str
    dropoff: str

# === API Endpoints ===
@app.get("/")
def root():
    api_configured = is_api_configured()
    return {
        "message": "Chaewon API is running!",
        "api_key_configured": api_configured,
        "routes": ["/register", "/login", "/route", "/ride/request", "/api/status"]
    }

@app.get("/api/status")
def api_status():
    """Check the status of Google Maps API configuration"""
    api_key = load_api_key() or os.getenv("GOOGLE_MAPS_API_KEY")
    return {
        "google_maps_api_configured": bool(api_key),
        "source": "app_config" if load_api_key() else "environment" if os.getenv("GOOGLE_MAPS_API_KEY") else "none",
        "key_preview": api_key[:10] + "..." if api_key and len(api_key) > 10 else None
    }

@app.post("/register")
def register(req: RegisterRequest):
    if req.password != req.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    if users_collection.find_one({"username": req.username}):
        raise HTTPException(status_code=409, detail="Username already exists")
    hashed_pw = hash_password(req.password)
    users_collection.insert_one({"username": req.username, "password": hashed_pw})
    return {"status": "success", "message": f"{req.username} registered successfully"}

@app.post("/login")
def login(req: LoginRequest):
    user = users_collection.find_one({"username": req.username})
    if not user or not verify_password(req.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"status": "authenticated", "message": f"Welcome, {req.username}"}

@app.post("/route")
def get_route(data: RouteRequest):
    # Check if API key is available
    api_key = load_api_key() or os.getenv("GOOGLE_MAPS_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=503, 
            detail="Google Maps API key not configured. Please configure it in the application settings."
        )
    
    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": data.origin,
        "destination": data.destination,
        "key": api_key
    }
    
    try:
        res = requests.get(url, params=params)
        if res.status_code != 200:
            raise HTTPException(status_code=500, detail="Google API error")
        
        directions = res.json()
        if directions.get("status") != "OK":
            if directions.get("status") == "REQUEST_DENIED":
                raise HTTPException(
                    status_code=403, 
                    detail="API key is invalid or does not have permission for Google Maps Directions API"
                )
            raise HTTPException(status_code=400, detail=directions.get("status"))
        
        leg = directions["routes"][0]["legs"][0]
        return {
            "distance": leg["distance"]["text"],
            "duration": leg["duration"]["text"],
            "start": leg["start_address"],
            "end": leg["end_address"]
        }
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Network error: {str(e)}")

@app.post("/ride/request")
def ride_request(req: RideRequest):
    user = users_collection.find_one({"username": req.user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "status": "pending",
        "ride": {
            "user_id": req.user_id,
            "pickup": req.pickup,
            "dropoff": req.dropoff,
            "estimate": "5–10 min"
        }
    }
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("Missing SECRET_KEY in .env")
