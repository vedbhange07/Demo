import cv2
import os
import mysql.connector
from datetime import datetime

# ----------------------------
# MySQL Connection
# ----------------------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Vedant@2005",   # CHANGE THIS
    database="attendance_db"
)

cursor = conn.cursor()

# ----------------------------
# Load Model
# ----------------------------
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer/trainer.yml")

faceCascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

names = os.listdir("dataset")

cam = cv2.VideoCapture(0)
cam.set(3, 640)
cam.set(4, 480)

while True:
    ret, frame = cam.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(gray, 1.2, 4)

    for (x, y, w, h) in faces:
        face = gray[y:y+h, x:x+w]
        face = cv2.resize(face, (200, 200))

        label, confidence = recognizer.predict(face)

        if confidence < 80:
            name = names[label]

            now = datetime.now()
            date = now.strftime("%Y-%m-%d")
            time = now.strftime("%H:%M:%S")

            cursor.execute(
                "SELECT * FROM attendance WHERE name=%s AND date=%s",
                (name, date)
            )

            if cursor.fetchone() is None:
                cursor.execute(
                    "INSERT INTO attendance (name, date, time) VALUES (%s,%s,%s)",
                    (name, date, time)
                )
                conn.commit()
                print(f"Attendance marked for {name}")

        else:
            name = "Unknown"

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
        cv2.putText(frame, name, (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

    cv2.imshow("Smart Attendance System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
conn.close()