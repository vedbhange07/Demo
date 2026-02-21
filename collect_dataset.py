import cv2
import os

# Ask student name
student_name = input("Enter Student Name: ")

# Create folder if not exists
dataset_path = "dataset"
student_path = os.path.join(dataset_path, student_name)

if not os.path.exists(student_path):
    os.makedirs(student_path)

# Load Haarcascade
face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

cam = cv2.VideoCapture(0)
cam.set(3, 640)
cam.set(4, 480)

count = 0

print("Collecting face samples... Look at camera")

while True:
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        count += 1

        face = gray[y:y+h, x:x+w]
        face = cv2.resize(face, (200, 200))

        cv2.imwrite(
            f"{student_path}/{count}.jpg",
            face
        )

        cv2.rectangle(img, (x, y), (x+w, y+h), (0,255,0), 2)

    cv2.imshow("Collecting Faces", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    elif count >= 50:
        break

print("Face collection complete!")

cam.release()
cv2.destroyAllWindows()