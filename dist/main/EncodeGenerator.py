import cv2
import os
import pickle
import face_recognition
from time import sleep
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

cred = credentials.Certificate("ServiceKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://lfr-attendence-system-default-rtdb.firebaseio.com/",
    'storageBucket' : "lfr-attendence-system.appspot.com"
})



#importing student images

folderpath = 'Images'
pathlist = os.listdir(folderpath)
imglist = []
studentIds = []

for path in pathlist:
    imglist.append(cv2.imread(os.path.join(folderpath,path)))
    studentIds.append(os.path.splitext(path)[0])

    filename = f'{folderpath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(filename)
    blob.upload_from_filename(filename)
# print(studentIds)


def findencodings(imageslist):
    encodelist=[]
    for img in imageslist:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodelist.append(encode)
    return encodelist

print("encoding started...")
encodelistknown = findencodings(imglist)
encodelistknownwithIds = [encodelistknown, studentIds]
print("Encoding complete")


print("Creating database file...")
file = open("EncodeFile.p","wb")
pickle.dump(encodelistknownwithIds,file)
file.close()
sleep(5)
print("File saved sucessfully")
