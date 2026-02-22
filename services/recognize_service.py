import cv2
import mysql.connector
from database.db import get_connection
import os

def recognize_face():
    if not os.path.exists("trainer/trainer.yml"):
        raise Exception("Model not trained yet!")

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("trainer/trainer.yml")

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    cam = cv2.VideoCapture(0)

    while True:
        ret, frame = cam.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            id, confidence = recognizer.predict(gray[y:y+h, x:x+w])

            if confidence < 70:
                conn = get_connection()
                cursor = conn.cursor()

                cursor.execute("SELECT name FROM students WHERE id=%s", (id,))
                result = cursor.fetchone()

                if result:
                    name = result[0]

                    cursor.execute(
                        "INSERT INTO attendance (student_id) VALUES (%s)",
                        (id,)
                    )
                    conn.commit()

                    cv2.putText(frame, name, (x, y-10),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.8, (0, 255, 0), 2)

                conn.close()
            else:
                cv2.putText(frame, "Unknown", (x, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.8, (0, 0, 255), 2)

            cv2.rectangle(frame, (x, y), (x+w, y+h),
                          (255, 0, 0), 2)

        cv2.imshow("Attendance System", frame)

        if cv2.waitKey(1) == 27:
            break

    cam.release()
    cv2.destroyAllWindows()