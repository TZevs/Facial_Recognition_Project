# Facial Recognition Attendance System
![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Figma](https://img.shields.io/badge/figma-%23F24E1E.svg?style=for-the-badge&logo=figma&logoColor=white)
![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
![Firebase](https://img.shields.io/badge/firebase-a08021?style=for-the-badge&logo=firebase&logoColor=black)
![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)
![YouTube](https://img.shields.io/badge/YouTube-%23FF0000.svg?style=for-the-badge&logo=YouTube&logoColor=white)
![macOS](https://img.shields.io/badge/mac%20os-000000?style=for-the-badge&logo=macos&logoColor=F0F0F0)

## Project Overview/Scenario
At the start of a class this system would be active and with the students images stored and econded.
When a student enters the classroom they would position their face infront of the camera(webcam)
until their info displays followed by the marked screen. This would register their attendance.

The system at the moment only has 3 images encoded of; myself, Andrew Lincoln and Emily Blunt. 

## How to Install and Run the Project
1. **Download or clone repository**
2. **Create Virtual Environment:**
```
python3 -m venv venv
```
3. **Activate venv** <br>
```
source venv/bin/activate
or
python3 venv/Scripts/activate
```
4. **Install Dependencies:**
```
pip install -r requirements.txt
```

## How to Use
1. **Set-up Firebase Realtime Database**
2. **Download private key json, add to directory**
3. **Add images to** ```/resources/images``` <br>
  3a. **Naming rules:** ```student_id.png```
4. **Add student data manually to DB or in** ```addDataToDB.py```:
```
data = {
  "student_id": {
      "name": "",
      "course": "",
      "starting_year": , 
      "total_attendance": 0,
      "year": ,
      "last_attendance_time": ""
  },
}

then
python3 addDataToDB.py
```
5. **Get Image Encodings:**
```
python3 encodeGenerator.py
```
6. **Run Project:**
```
python3 main.py
```

### Credits
Based on this tutorial: <br> 
[Face Recognition with Real Time Database | 2 Hour Course | Computer Vision](https://www.youtube.com/watch?v=iBomaK2ARyI)
