# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os, requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# === MongoDB Setup ===
from pymongo import MongoClient
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client["chaewon_db"]
users_collection = db["users"]

# === Google Maps API ===
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "YOUR_API_KEY")

# === FastAPI App ===
app = FastAPI(title="Chaewon Meet & Greet API", version="1.0.0")

# --------------------
# Models
# --------------------
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

# --------------------
# Utils (Hashing)
# --------------------
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(pw): return pwd_context.hash(pw)
def verify_password(pw, hashed): return pwd_context.verify(pw, hashed)

# --------------------
# Endpoints
# --------------------

@app.post("/register")
def register(req: RegisterRequest):
    if req.password != req.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    if users_collection.find_one({"username": req.username}):
        raise HTTPException(status_code=409, detail="Username already exists")
    hashed_pw = hash_password(req.password)
    users_collection.insert_one({"username": req.username, "password": hashed_pw})
    return {"status": "success", "message": f"{req.username} registered."}

@app.post("/login")
def login(req: LoginRequest):
    user = users_collection.find_one({"username": req.username})
    if not user or not verify_password(req.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"status": "authenticated", "message": f"Welcome, {req.username}"}

@app.post("/route")
def get_route(data: RouteRequest):
    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": data.origin,
        "destination": data.destination,
        "key": GOOGLE_MAPS_API_KEY
    }
    res = requests.get(url, params=params)
    if res.status_code != 200:
        raise HTTPException(status_code=500, detail="Google API error")
    directions = res.json()
    if directions.get("status") != "OK":
        raise HTTPException(status_code=400, detail=directions.get("status"))
    leg = directions["routes"][0]["legs"][0]
    return {
        "distance": leg["distance"]["text"],
        "duration": leg["duration"]["text"],
        "start": leg["start_address"],
        "end": leg["end_address"]
    }

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
            "estimate": "5-10 min"
        }
    }

@app.get("/")
def root():
    return {
        "message": "Chaewon API Running",
        "routes": ["/register", "/login", "/route", "/ride/request"]
    }
