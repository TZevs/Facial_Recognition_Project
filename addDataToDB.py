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
    "123321": {
        "name": "Thalia Evans",
        "course": "Software Engineering",
        "starting_year": 2023, 
        "total_attendance": 10,
        "standing": "G",
        "year": 3,
        "last_attendance_time": "2024-12-22 10:57:00"
    },
    "321645": {
        "name": "Andrew Lincoln",
        "course": "Software Engineering",
        "starting_year": 2023, 
        "total_attendance": 12,
        "standing": "G",
        "year": 3,
        "last_attendance_time": "2024-12-22 11:03:00"
    },
    "852741": {
        "name": "Emily Blunt",
        "course": "Software Engineering",
        "starting_year": 2023, 
        "total_attendance": 8,
        "standing": "OK",
        "year": 3,
        "last_attendance_time": "2024-12-22 11:04:00"
    }
}

# Accesses the key (id) and the value (data json) in the dictionary
for key, value in data.items():
    ref.child(key).set(value)