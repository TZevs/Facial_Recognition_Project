# Facial Recognition Attendance System
A facial recognition application that will identify students, as they face the camera, and log them as in attendance without any interference or input from the teacher. 

---
## 🎓 About 
A real-time facial recognition attendance system built with Python. Using a webcam feed, the system detects and identifies students, displays their profile info, and automatically logs their attendance to a Firebase Realtime Database - removing the need for manual registration in classes.

🫟**Problem:** 

🚪**Approach:** 

🚦**Status:**

### ✨ Features
- 

## How It Works
1. The webcam captures a live video feed and detects faces in each frame using `face_recognition`.
2. Detected faces are compared against a set of pre-encoded student images stored in `EncodeFile.p`.
3. Once a face is confirmed across several consecutive frames, the student's data is fetched from Firebase.
4. Their profile (name, course, year, attendance count) is displayed on-screen, their attendance is updated in the database, and the UI transitions through active -> info -> marked states.
5. Students already marked in the current session are prevented from being counted twice.

---
### 🛠️ Tech Stack
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
<br>
![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
<br>
![Firebase](https://img.shields.io/badge/firebase-a08021?style=for-the-badge&logo=firebase&logoColor=black)
![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Figma](https://img.shields.io/badge/figma-%23F24E1E.svg?style=for-the-badge&logo=figma&logoColor=white)
![YouTube](https://img.shields.io/badge/YouTube-%23FF0000.svg?style=for-the-badge&logo=YouTube&logoColor=white)

---
### 🏛️ Project Structure
```
Face_Recognition_Project/
├── resources/
│   ├── images/          # Student photos (named by student ID)
│   └── UI/              # Background UI assets for each mode
├── main.py              # Core application loop and recognition logic
├── encodeGenerator.py   # Generates and saves face encodings
├── addDataToDB.py       # Populates Firebase with student data
├── EncodeFile.p         # Serialised face encodings (generated)
├── firebaseKey.json     # Firebase service account key (not tracked)
├── requirements.txt     # Python dependencies
└── .gitignore
```
--- 
## 📦 Setup
### Installation 
```bash
git clone https://github.com/TZevs/Face_Recognition_Project.git
cd Face_Recognition_Project
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
> **Note:** `dlib` (required by `face_recognition`) may require additional build tools on some systems. See the [dlib installation guide](http://dlib.net/compile.html) if you encounter errors.

### Usage
#### Configure Firebase
- Create a project with Realtime Database enabled. **[Firebase Docs](https://firebase.google.com/)**
- In your Firebase project, enable **Realtime Database**.
- Download your **service account private key** JSON file and rename it to your `firebaseKey.json`.
- Place `firebaseKey.json` in the root of the project directory.
- Update the `databaseURL` in `main.py` to match your Firebase project's database URL.

#### Add student images 
Place student photos in `resources/images/`. Each image must follow the naming convention:
```
<student_id>.png
```
For example: `21004321.png`

#### Add student data to databse
Edit `addDataToDB.py` to populate your student records:
```python
data = {
  "21004321": {
      "name": "Jane Smith",
      "course": "Software Engineering",
      "starting_year": 2022, 
      "total_attendance": 0,
      "year": 2,
      "last_attendance_time": ""
  },
}
```
Then run:
```bash
python3 addDataToDB.py
```
This processes all images in `resources/images/` and writes the encodings to `EncodeFile.p`.

#### Run Locally:
```bash
python3 main.py
```
Point a student's face at the webcam. Once identified, their info will appear on screen and their attendance will be logged.
Press `ESC` to exit.

---
## 🔍 Known Issues & Improvements to be Made
- 

---
## Credits
Built following the tutorial: [Face Recognition with Real Time Database | 2 Hour Course | Computer Vision](https://www.youtube.com/watch?v=iBomaK2ARyI) by Murtaza's Workshop.

--- 
## Licence
This project is licensed under the MIT License.
