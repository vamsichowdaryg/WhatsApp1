from fastapi import FastAPI
from pydantic import BaseModel
import json
import os
 
app = FastAPI()
 
DATA_FILE = "User.json"
 
# Load users from file
def load_users():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}
 
# Save users to file
def save_users(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)
 
# In-memory storage for runtime, loaded from file
users = load_users()
 
@app.get("/")
def root():
    return {"message": "Welcome to the FastAPI service!"}
 
@app.get("/verify-smartcard/{smartcard_number}")
def verify_smartcard(smartcard_number: str):
    if smartcard_number in users:
        return {"valid": True}
    return {"valid": False, "error": "Smart Card Number not found"}
 
@app.get("/verify-phone/{smartcard_number}/{phone_number}")
def verify_phone(smartcard_number: str, phone_number: str):
    user = users.get(smartcard_number)
    if user and user["phone"] == phone_number:
        return {"valid": True}
    return {"valid": False, "error": "Phone number does not match for given Smart Card"}
 
class Movie(BaseModel):
    title: str
    genre: str
    duration: int
 
@app.post("/add-movie/{smartcard_number}")
def add_movie(smartcard_number: str, movie: Movie):
    if smartcard_number not in users:
        return {"error": "Invalid Smart Card Number"}
    return {"message": f"Movie '{movie.title}' added successfully to {smartcard_number}"}
 
@app.get("/balance/{smartcard_number}")
def check_balance(smartcard_number: str):
    user = users.get(smartcard_number)
    if user:
        return {"smartcard_number": smartcard_number, "balance": user["balance"]}
    return {"error": "Smart Card Number not found"}
 
class TopUp(BaseModel):
    amount: int
 
@app.post("/top-up/{smartcard_number}")
def top_up(smartcard_number: str, data: TopUp):
    user = users.get(smartcard_number)
    if user:
        user["balance"] += data.amount
        save_users(users)  # Save to file
        return {"smartcard_number": smartcard_number, "new_balance": user["balance"]}
    return {"error": "Smart Card Number not found"}
 
@app.get("/all-users")
def get_all_users():
    return users