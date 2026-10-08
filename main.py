import cv2
import pickle
import face_recognition
import numpy as np
import asyncio
import datetime
import firebase_admin
from firebase_admin import credentials, db
import json

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

# --- Modes ---
MODE_ACTIVE = 0
MODE_INFO = 1
MODE_MARKED = 2
MODE_ALREADY_MARKED = 3

# Times for frames to be displayed
FPS = 30
MODE_DURATION = {
    MODE_INFO: 2 * FPS,
    MODE_MARKED: FPS,
    MODE_ALREADY_MARKED: FPS
}

# --- UI ---
backgrounds = {
    MODE_ACTIVE: cv2.imread("resources/UI/active.png"),
    MODE_INFO: cv2.imread("resources/UI/info.png"),
    MODE_MARKED: cv2.imread("resources/UI/marked.png"),
    MODE_ALREADY_MARKED: cv2.imread("resources/UI/alreadyMarked.png")
}

# --- State ---
modeType = MODE_ACTIVE
mode_counter = 0

current_id = None
current_info = None

marked_students = []

confirm_counter = 0
missed_counter = 0

CONFIRM_FRAMES = 5
MAX_MISSED_FRAMES = 10

# --- Helpers ---
def set_mode(new_mode):
    global modeType, mode_counter
    if new_mode != modeType:
        modeType = new_mode
        mode_counter = 0

async def fetch_student(student_id):
# Inside corourtine object
    # Runs blocking Firebase call in diff thread
    return await asyncio.to_thread(
        lambda: ref.child(student_id).get()
    )

async def update_attendance(student_id, total):
    d = datetime.datetime.now()
    await asyncio.to_thread(
        lambda: ref.child(student_id).update({
            "total_attendance": total + 1,
            "last_attendance": d.strftime("%x %X")
        })
    )

# --- Load Encodings ---
file = open("EncodeFile.p", "rb")
encodeListKnown, studentIds = pickle.load(file)
file.close()

# --- Camera ---
frame = cv2.VideoCapture(0)
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# --- Main Loop ---
while True:
    # Reads a frame from the webcam
    success, img = frame.read()        
    if not success: 
        continue

    # Set background template, mode_active default
    imgBackground = backgrounds.get(modeType, backgrounds[MODE_ACTIVE]).copy()
    img = cv2.resize(img, (530, 300))

    # Pre-processing for face recognition - reduces image size by 4
    imgS = cv2.resize(img, (0,0), None, 0.25, 0.25)
    # Converts opencv BGR to RGB for face_recognition
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    # Detects face - returns list of (top, right, bottom, left)
    faceCurrentFrame = face_recognition.face_locations(imgS)
    # Converts detected face
    encodeCurrentFrame = face_recognition.face_encodings(imgS, faceCurrentFrame)

    # Overlay webcam and card onto background [starting & ending point of height, width]
    imgBackground[145:145+300, 40:40+530] = img

    # Tracks whether any face matched in this frame
    recognised = False

    # --- Recognition Logic ---
    for encodeFace, faceLoc in zip(encodeCurrentFrame, faceCurrentFrame):
        # --- Draw rectangle on ALL faces ---
        # Detected face - multiply coordinates by 4 (to original size)
        y1, x2, y2, x1 = [v * int(1 / 0.25) for v in faceLoc]
        cv2.rectangle(imgBackground, (65+x1, 145+y1), (65+x2, 145+y2), (0,255,0), 2)

        # Face recognition: Comparison and the lower distance = better match
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace) # Returns list of booleans
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace) # Returns distances
        matchIndex = np.argmin(faceDis) # Finds index of best match
        
        if matches[matchIndex]:
            recognised = True
            temp_id = studentIds[matchIndex]

            # --- Confirmation Logic ---
            if current_id == temp_id:
                confirm_counter += 1
            else :
                confirm_counter = 1
                current_id = temp_id
            
            missed_counter = 0

            # --- Accept Identity --- 
            if confirm_counter == CONFIRM_FRAMES:
                current_info = loop.run_until_complete(fetch_student(current_id))

                if not current_id in marked_students:
                    set_mode(MODE_INFO)
                    marked_students.append(current_id)
                else:
                    set_mode(MODE_ALREADY_MARKED)
            break

    # --- State(Mode) Transitions ---
    mode_counter += 1

    if modeType == MODE_INFO and mode_counter > MODE_DURATION[MODE_INFO]:
        # Pauses main loop till thread complete
        loop.run_until_complete(
            update_attendance(current_id, current_info["total_attendance"])
        )
        set_mode(MODE_MARKED)

    elif modeType in (MODE_MARKED, MODE_ALREADY_MARKED) and mode_counter > MODE_DURATION[modeType]:
        set_mode(MODE_ACTIVE)
        current_id = None
        current_info = None
        confirm_counter = 0

    # --- Missed Frame Reset ---
    if not recognised:
        missed_counter += 1
        if missed_counter > MAX_MISSED_FRAMES:
            set_mode(MODE_ACTIVE)
            current_id = None
            current_info = None
            confirm_counter = 0
    
    # Keep the text displayed if the info mode is active
    if modeType == MODE_INFO and current_info is not None:
        cv2.putText(imgBackground, str(current_info["total_attendance"] + 1), (709, 125), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0), 1)
        cv2.putText(imgBackground, f"ID: {current_id}", (700, 290), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0,0), 1)
        cv2.putText(imgBackground, current_info["name"], (700, 355), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0,0), 1)
        cv2.putText(imgBackground, current_info["course"], (700, 420), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0,0), 1)

    cv2.imshow("Face Attendance", imgBackground)

    # Exit loop with ESC
    if cv2.waitKey(1) & 0xFF == 27:
        break

frame.release()
cv2.destroyAllWindows()
