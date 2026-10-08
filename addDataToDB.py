import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Load Firebase credentials from JSON file
with open("firebaseKey.json", "r") as f:
    cred_data = json.load(f)

db_url = cred_data.get("databaseURL")

# --- Firebase ---
cred = credentials.Certificate(cred_data)
firebase_admin.initialize_app(cred, {
    "databaseURL": db_url
})

ref = db.reference("Students")

data = {
    "675657": {
        "name": "",
        "course": "",
        "starting_year": 2023, 
        "total_attendance": 0,
        "year": 3,
        "last_attendance_time": "2024-12-22 10:57:00"
    }
}

# Accesses the key (id) and the value (data json) in the dictionary
for key, value in data.items():
    ref.child(key).set(value)