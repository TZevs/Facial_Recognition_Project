import cv2
import pickle
import face_recognition
import numpy as np
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Access to private key for Firebase project
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://facerecogattendance-b8673-default-rtdb.europe-west1.firebasedatabase.app/"
})

# Initialize webcam
frame = cv2.VideoCapture(0)

# Import ui
imgBackground = cv2.imread("resources/UI/background.png")
folderCardList = [
    cv2.imread("resources/UI/active.png"),
    cv2.imread("resources/UI/info.png"),
    cv2.imread("resources/UI/marked.png"),
    cv2.imread("resources/UI/alreadyMarked.png")
]

# Variables for changing the UI and reading/writing data
modeType = 0
counter = 0
id = 0
studentCache = dict()

# Box size from Figma
webcam_BOX_W = 414
webcam_BOX_H = 311

card_BOX_W = 300
card_BOX_H = 410

# Resize cards to be the same
for i in range(len(folderCardList)):
    folderCardList[i] = cv2.resize(folderCardList[i], (card_BOX_W, card_BOX_H))


# Load the encoding file. rb = reading
print("Loading Encode File...")
file = open("EncodeFile.p", "rb")
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
# print(studentIds)
print("Encode File Loaded")

try: 
    while True:
        success, img = frame.read()        
        img = cv2.resize(img, (webcam_BOX_W, webcam_BOX_H))

        # Size of the detected image
        imgS = cv2.resize(img,(0,0),None,0.25,0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        # Location of the face in frame
        faceCurrentFrame = face_recognition.face_locations(imgS)
        # Encode the detected face, not whole image
        encodeCurrentFrame = face_recognition.face_encodings(imgS, faceCurrentFrame)

        # Overlay webcam onto background [starting & ending point of height, width]
        imgBackground[145:145+webcam_BOX_H, 65:65+webcam_BOX_W] = img
        imgBackground[45:45+card_BOX_H, 585:585+card_BOX_W] = folderCardList[modeType]

        # zip method to loop through the 2 lists together
        for encodeFace, faceLoc in zip(encodeCurrentFrame, faceCurrentFrame):
            # Get the face location
            y1, x2, y2, x1 = faceLoc
            # Multiply by 4 as we scaled down by 4
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            cv2.rectangle(imgBackground, (65+x1, 145+y1), (65+x2, 145+y2), (255,0,0), 2)

            # Face recognition: Comparison and the lower the distance the better the match
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            # Gets the index of the best match
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]: 
                # print("Known Face Detected")
                cv2.rectangle(imgBackground, (65+x1, 145+y1), (65+x2, 145+y2), (0,255,0), 2)

                id = studentIds[matchIndex]

                # if counter == 0:
                #     studentInfo = db.reference(f"Students/{id}").get()
                #     counter = 1
                #     modeType = 1
                
                if id not in studentCache:
                    studentCache[id] = db.reference(f"Students/{id}").get()
                    modeType = 1
                
                studentInfo = studentCache[id]

            cv2.putText(imgBackground, str(id), (660, 320), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0,0), 1)
            cv2.putText(imgBackground, str(studentInfo["name"]), (660, 350), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0,0), 1)

        cv2.imshow("Face Attendance", imgBackground)
        cv2.waitKey(1)
# Allows Ctrl+C to exit the loop
except KeyboardInterrupt: 
    pass
