import os
import cv2

def collect_dataset(student_id, name):
    dataset_path = "dataset"

    if not os.path.exists(dataset_path):
        os.makedirs(dataset_path)

    # 🔥 SAFE FOLDER NAME (no spaces)
    safe_name = name.replace(" ", "_")
    student_folder = os.path.join(dataset_path, f"{student_id}_{safe_name}")

    if not os.path.exists(student_folder):
        os.makedirs(student_folder)

    cam = cv2.VideoCapture(0)
    sampleNum = 0

    while True:
        ret, img = cam.read()
        if not ret:
            break

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        sampleNum += 1
        file_path = os.path.join(student_folder, f"User.{student_id}.{sampleNum}.jpg")
        cv2.imwrite(file_path, gray)

        cv2.imshow("Capturing Faces", img)

        if cv2.waitKey(1) == 13 or sampleNum >= 20:
            break

    cam.release()
    cv2.destroyAllWindows()