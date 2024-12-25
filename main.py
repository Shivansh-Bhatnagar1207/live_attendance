import os  # helps with file/folder management
import cv2  # computer vision
import pickle  # helps with file creation and update
import face_recognition_models  # helps with face recognition and comparison of data
import numpy as np
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime


cred = credentials.Certificate("ServiceKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://lfr-attendence-system-default-rtdb.firebaseio.com/",
    'storageBucket': "lfr-attendance-system.appspot.com"
})
bucket = storage.bucket()

cap = cv2.VideoCapture(0)  # selecting the source of the camera
cap.set(3, 640)  # setting up the height of webcam
cap.set(4, 480)  # setting up the width of webcam

imgbackground = cv2.imread("resources/background.png")  # the background image

# importing the mode images into a list
FolderModePath = "resources/modes"
ModePathList = os.listdir(FolderModePath)
imgModeList = []
for path in ModePathList:
    imgModeList.append(cv2.imread(os.path.join(FolderModePath, path)))
# print(len(imgModeList))


# Load the encoding file
print("Loading encode file")
file = open("EncodeFile.p", "rb")
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
print("Encoded File Loaded")
# print(studentIds)

modetype = 0
counter = 0
rollno = 0
imgStudents =[]
while True:
    success, img = cap.read()
    # reducing the size of the webcam frame to compute faster
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)  # changing the image from BGR (standard camera format) to RGB (suitable format)

    facecurframe = face_recognition_models.face_locations(imgS)  # detection of face
    encodecurframe = face_recognition_models.face_encodings(imgS, facecurframe)  # distance of the face

    imgbackground[162: 162 + 480, 55: 55 + 640] = img  # position of the webcam on the background image
    imgbackground[44: 44 + 633, 808: 808 + 414] = imgModeList[modetype]  # position of the modes on the background image

    # matching the faces from the frame and database to record attendence
    if facecurframe:
        for encodeface, faceloc in zip(encodecurframe, facecurframe):
            matches = face_recognition_models.compare_faces(encodeListKnown, encodeface)
            faceDis = face_recognition_models.face_distance(encodeListKnown, encodeface)
            # print("matches", matches)
            # print("matches", matches)
            # print("facedistance", facedistapip nce)

            matchIndex = np.argmin(faceDis)
            # print("Match Index ", matchIndex)
            if matches[matchIndex]:
                # print(studentIds[matchIndex])
                rollno = studentIds[matchIndex]
                if counter == 0:
                    cvzone.putTextRect(imgbackground,"Loading",(275,400))
                    cv2.imshow("Face Attendence", imgbackground)
                    cv2.waitKey(1)
                    counter = 1
                    modetype = 1
        if counter != 0:

            if counter == 1:
                #get the data
                studentinfo = db.reference(f'students/{rollno}').get()
                print(studentinfo)
               #Update data of attendence
                datetimeObject = datetime.strptime(studentinfo['Last_Attendence'],'%Y-%m-%d %H:%M:%S')
                secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                print(secondsElapsed)
                if secondsElapsed>30:
                    ref = db.reference(f'students/{rollno}')
                    studentinfo['Total_Attendencec'] +=1
                    ref.child('Total_Attendencec').set(studentinfo['Total_Attendencec'])
                    ref.child('Last_Attendence').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    modetype =3
                    imgbackground[44: 44 + 633, 808: 808 + 414] = imgModeList[modetype]
                    counter = 0
            if modetype != 3:
                if 10<counter<=20:
                    modetype = 2
                imgbackground[44: 44 + 633, 808: 808 + 414] = imgModeList[modetype]

                if counter<10:
                    cv2.putText(imgbackground, str(studentinfo['Total_Attendencec']), (861, 125), cv2.FONT_HERSHEY_COMPLEX, 1,(255, 255, 255), 1)
                    cv2.putText(imgbackground, str(studentinfo['Branch']), (1006, 550), cv2.FONT_HERSHEY_COMPLEX, 0.5,(255, 255, 255), 1)
                    cv2.putText(imgbackground, str(rollno), (1006,493), cv2.FONT_HERSHEY_COMPLEX, 0.5,(255, 255, 255), 1)
                    cv2.putText(imgbackground, str(studentinfo['Specilization']), (910,625), cv2.FONT_HERSHEY_COMPLEX, 0.6,(100,100,100), 1)
                    cv2.putText(imgbackground, str(studentinfo['Batch']), (1108,625), cv2.FONT_HERSHEY_COMPLEX, 0.6,(100,100,100), 1)
                    cv2.putText(imgbackground, str(studentinfo['Course']), (1008,625), cv2.FONT_HERSHEY_COMPLEX, 0.6,(100,100,100), 1)

                    (w,h),_ =cv2.getTextSize(studentinfo['Name'],cv2.FONT_HERSHEY_COMPLEX,1,1)
                    offset = (414 - w )//2
                    cv2.putText(imgbackground, str(studentinfo['Name']), (808+offset, 445), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)


                # imgbackground[175:175 + 216, 909:909 + 216] = imgStudent

                counter += 1
                if counter>20:
                    modetype =0
                    imgbackground[44: 44 + 633, 808: 808 + 414] = imgModeList[modetype]
                    studentinfo=[]
                    counter=0
    else:
        modetype =0
        counter =0


    cv2.imshow("Face Attendence", imgbackground)
    cv2.waitKey(1)
