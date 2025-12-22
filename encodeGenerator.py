import cv2
import face_recognition
import pickle
import os

# Import images for encoding
imgFolderPath = "resources/images"
pathList = os.listdir(imgFolderPath)
imgList = []
studentIds = []
for imgPath in pathList:
    imgList.append(cv2.imread(os.path.join(imgFolderPath, imgPath)))
    imgId = os.path.splitext(imgPath)[0]
    studentIds.append(imgId)
# print(len(imgList))

# Generate image encodings
def findEncodings(imagesList): 
    encodeList = []

    # Loop through all images and encode them
    for img in imagesList:
        # Convert BGR to RGB as face recognition uses RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList

print("Encoding Started...")
encodeListKnown = findEncodings(imgList)
print(encodeListKnown[0])
encodeListKnownWithIds = [encodeListKnown, studentIds]
print("Encoding Complete")

# Save encoded images with IDs to file
file = open("EncodeFile.p", "wb")
pickle.dump(encodeListKnownWithIds, file)
file.close()
print("File Saved")