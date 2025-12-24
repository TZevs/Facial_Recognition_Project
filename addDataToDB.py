import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Access to private key for Firebase project
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://facerecogattendance-b8673-default-rtdb.europe-west1.firebasedatabase.app/"
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