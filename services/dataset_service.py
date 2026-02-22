import cv2
import os

def collect_dataset(student_id, name):
    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        print("❌ Camera not working")
        return

    dataset_path = f"dataset/{student_id}_{name}"

    if not os.path.exists(dataset_path):
        os.makedirs(dataset_path)

    count = 0

    print("📸 Starting dataset collection...")

    while True:
        ret, frame = cam.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        cv2.imshow("Collecting Faces - Press ESC to Stop", frame)

        count += 1

        file_path = f"{dataset_path}/User.{student_id}.{count}.jpg"
        cv2.imwrite(file_path, gray)

        if count >= 30:
            break

        if cv2.waitKey(1) == 27:
            break

    cam.release()
    cv2.destroyAllWindows()

    print("✅ Dataset Collected Successfully")