import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
cred = credentials.Certificate("ServiceKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://lfr-attendence-system-default-rtdb.firebaseio.com/"
})


ref = db.reference('students')

data = {
    "2104500100012" :
        {
            "Name" : "Ashish Yadav",
            "Course" : "B.Tech",
            "Branch" : "CSE",
            "Specilization" : "IOT",
            "Total_Attendencec" : 10,
            "Batch" : 2021,
            "Last_Attendence" : "2023-06-30 00:12:13"
        },
    "2104500100019" :
        {
            "Name" : "Harivansh Shankdhar",
            "Course" : "B.Tech",
            "Branch" : "CSE",
            "Specilization" : "IOT",
            "Total_Attendencec" : 10,
            "Batch" : 2021,
            "Last_Attendence" : "2023-06-30 00:12:13"
        },
    "2104500100021" :
        {
            "Name" : "Prateep Rai",
            "Course" : "B.Tech",
            "Branch" : "CSE",
            "Specilization" : "CSS",
            "Total_Attendencec" : 10,
            "Batch" : 2021,
            "Last_Attendence" : "2023-06-30 00:12:13"
        },
    "2104500100026" :
        {
            "Name" : "Lakshya Upadhyay",
            "Course" : "B.Tech",
            "Branch" : "CSE",
            "Specilization" : "CSS",
            "Total_Attendencec" : 10,
            "Batch" : 2021,
            "Last_Attendence" : "2023-06-30 00:12:13"
        },
    "2104500100035" :
        {
            "Name" : "Mohd Maaz",
            "Course" : "B.Tech",
            "Branch" : "CSE",
            "Specilization" : "CSS",
            "Total_Attendencec" : 10,
            "Batch" : 2021,
            "Last_Attendence" : "2023-06-30 00:12:13"
        },
    "2104500100045" :
        {
            "Name" : "Priyanshi Agarwal",
            "Course" : "B.Tech",
            "Branch" : "CSE",
            "Specilization" : "IOT",
            "Total_Attendencec" : 10,
            "Batch" : 2021,
            "Last_Attendence" : "2023-06-30 00:12:13"
        },
    "2104500100054" :
        {
            "Name" : "Soumya Mishra",
            "Course" : "B.Tech",
            "Branch" : "CSE",
            "Specilization" : "CSS",
            "Total_Attendencec" : 10,
            "Batch" : 2021,
            "Last_Attendence" : "2023-06-30 00:12:13"
        },
    "2104500100057" :
        {
            "Name" : "Shivam Panday",
            "Course" : "B.Tech",
            "Branch" : "CSE",
            "Specilization" : "IOT",
            "Total_Attendencec" : 10,
            "Batch" : 2021,
            "Last_Attendence" : "2023-06-30 00:12:13"
        },
    "2104500100058" :
        {
            "Name" : "Shivansh Bhatnagar",
            "Course" : "B.Tech",
            "Branch" : "CSE",
            "Specilization" : "IOT",
            "Total_Attendencec" : 10,
            "Batch" : 2021,
            "Last_Attendence" : "2023-06-30 00:12:13"
        }
}


for key,value in data.items():
    ref.child(key).set(value)