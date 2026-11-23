import argparse
import firebase_admin
from firebase_admin import credentials, firestore

SAMPLE_STUDENTS = [
    {"id": "20210045", "name": "Ahmed Mohamed", "major": "CCAS", "email": "20210045@ngu.edu.eg", "level": "Year 4"},
    {"id": "202201565", "name": "Ahmed Sherif Kamal", "major": "CCAS", "email": "202201565@ngu.edu.eg", "level": "Year 4"},
    {"id": "20210087", "name": "Mariam Adel", "major": "Computer Engineering", "email": "20210087@ngu.edu.eg", "level": "Year 3"},
    {"id": "20210112", "name": "Omar Hany", "major": "Electronics Engineering", "email": "20210112@ngu.edu.eg", "level": "Year 3"},
    {"id": "20220031", "name": "Nour Youssef", "major": "Biomedical Informatics", "email": "20220031@ngu.edu.eg", "level": "Year 2"},
]

SAMPLE_PROFESSORS = [
    {
        "id": "khaled_hassan",
        "name": "Dr. Khaled Hassan",
        "department": "CCAS - Robotics and Autonomous Systems",
        "office": "Office Room C314 - Robotics Faculty Office",
        "email": "khaled.hassan@ngu.edu.eg",
        "schedule": [
            {"day": "Sunday", "start": "09:00", "end": "10:30", "location": "Lab Room R101 - Robotics Lab", "activity": "Robotics Lecture", "course": "ROB401"},
            {"day": "Sunday", "start": "11:00", "end": "12:30", "location": "Lecture Room C203", "activity": "Mobile Robotics Tutorial", "course": "ROB401"},
            {"day": "Monday", "start": "10:00", "end": "12:00", "location": "Lab Room ASL-2 - Autonomous Systems Lab", "activity": "Graduation Project Supervision", "course": "GP"},
            {"day": "Tuesday", "start": "12:00", "end": "13:30", "location": "Lecture Room C105", "activity": "Navigation Systems Lecture", "course": "ROB420"},
            {"day": "Wednesday", "start": "09:00", "end": "10:30", "location": "Lab Room R101 - Robotics Lab", "activity": "Robot Perception Lab", "course": "ROB430"},
            {"day": "Thursday", "start": "13:00", "end": "15:00", "location": "Lab Room R101 - Robotics Lab", "activity": "Robotics Practical Session", "course": "ROB401"},
        ],
    },
    {
        "id": "sara_nabil",
        "name": "Dr. Sara Nabil",
        "department": "Computer Engineering",
        "office": "Office Room B203 - Computer Engineering Faculty Office",
        "email": "sara.nabil@ngu.edu.eg",
        "schedule": [
            {"day": "Sunday", "start": "10:00", "end": "11:30", "location": "Lecture Room B105", "activity": "Database Systems Lecture", "course": "CSE302"},
            {"day": "Monday", "start": "09:00", "end": "10:30", "location": "Lab Room B214 - Software Lab", "activity": "Software Engineering Lab", "course": "CSE310"},
            {"day": "Tuesday", "start": "11:00", "end": "12:30", "location": "Lecture Room B210", "activity": "Software Engineering Lecture", "course": "CSE310"},
            {"day": "Wednesday", "start": "12:00", "end": "14:00", "location": "Lab Room B216 - Computer Lab 2", "activity": "Database Lab", "course": "CSE302"},
            {"day": "Thursday", "start": "09:00", "end": "10:30", "location": "Lecture Room B106", "activity": "Advanced SQL Lecture", "course": "CSE408"},
        ],
    },
    {
        "id": "mohamed_ali",
        "name": "Dr. Mohamed Ali",
        "department": "Electronics Engineering",
        "office": "Office Room C305 - Electronics Faculty Office",
        "email": "mohamed.ali@ngu.edu.eg",
        "schedule": [
            {"day": "Sunday", "start": "12:00", "end": "14:00", "location": "Lab Room E201 - Electronics Lab", "activity": "Digital Communications Lab", "course": "ECE405"},
            {"day": "Monday", "start": "13:00", "end": "14:30", "location": "Lecture Room C101", "activity": "Digital Communications Lecture", "course": "ECE405"},
            {"day": "Tuesday", "start": "09:00", "end": "10:30", "location": "Lab Room S110 - Signals Lab", "activity": "Signals Practical", "course": "ECE210"},
            {"day": "Wednesday", "start": "10:30", "end": "12:00", "location": "Lecture Room C209", "activity": "Signals Tutorial", "course": "ECE210"},
            {"day": "Thursday", "start": "11:00", "end": "12:30", "location": "Lecture Room C101", "activity": "Wireless Communication Lecture", "course": "ECE430"},
        ],
    },
    {
        "id": "mona_youssef",
        "name": "Dr. Mona Youssef",
        "department": "AI and Data Science",
        "office": "Office Room B312 - AI Faculty Office",
        "email": "mona.youssef@ngu.edu.eg",
        "schedule": [
            {"day": "Sunday", "start": "13:00", "end": "15:00", "location": "Lab Room A301 - AI Lab", "activity": "Machine Learning Lab", "course": "AI301"},
            {"day": "Monday", "start": "11:00", "end": "12:30", "location": "Lecture Room B107", "activity": "Machine Learning Lecture", "course": "AI301"},
            {"day": "Tuesday", "start": "14:00", "end": "16:00", "location": "Lecture Room B107", "activity": "Deep Learning Lecture", "course": "AI410"},
            {"day": "Wednesday", "start": "09:00", "end": "11:00", "location": "Lab Room A301 - AI Lab", "activity": "Computer Vision Practical", "course": "AI420"},
            {"day": "Thursday", "start": "12:00", "end": "13:30", "location": "Lecture Room B309", "activity": "Data Science Seminar", "course": "AI390"},
        ],
    },
    {
        "id": "omar_fathy",
        "name": "Dr. Omar Fathy",
        "department": "Networks and Cybersecurity",
        "office": "Office Room A220 - Networks Faculty Office",
        "email": "omar.fathy@ngu.edu.eg",
        "schedule": [
            {"day": "Sunday", "start": "11:00", "end": "12:30", "location": "Lecture Room A110", "activity": "Computer Networks Lecture", "course": "NET301"},
            {"day": "Monday", "start": "12:00", "end": "13:30", "location": "Lab Room N201 - Network Lab", "activity": "Routing Lab", "course": "NET301"},
            {"day": "Tuesday", "start": "10:00", "end": "11:30", "location": "Lecture Room A112", "activity": "Cybersecurity Lecture", "course": "SEC320"},
            {"day": "Wednesday", "start": "13:00", "end": "14:30", "location": "Lab Room S205 - Security Lab", "activity": "Cryptography Lab", "course": "SEC410"},
            {"day": "Thursday", "start": "09:00", "end": "10:30", "location": "Lecture Room A110", "activity": "Network Security Lecture", "course": "SEC330"},
        ],
    },
]


def reset_collection(db, collection_name):
    docs = list(db.collection(collection_name).stream())
    if not docs:
        return
    batch = db.batch()
    for doc in docs:
        batch.delete(doc.reference)
    batch.commit()
    print(f"Cleared {len(docs)} old documents from {collection_name}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--service-account", default="serviceAccountKey.json")
    parser.add_argument("--keep-old-professors", action="store_true", help="Do not clear the professors collection before seeding")
    args = parser.parse_args()

    cred = credentials.Certificate(args.service_account)
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    for student in SAMPLE_STUDENTS:
        db.collection("students").document(student["id"]).set(student)
        print(f"Added student {student['id']} - {student['name']}")

    if not args.keep_old_professors:
        reset_collection(db, "professors")

    for professor in SAMPLE_PROFESSORS:
        db.collection("professors").document(professor["id"]).set(professor)
        print(f"Added professor {professor['name']}")

    print("Sample database seeding completed.")


if __name__ == "__main__":
    main()
