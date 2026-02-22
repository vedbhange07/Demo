import cv2
import os
import numpy as np

def train_model():
    dataset_path = "dataset"
    faces = []
    ids = []

    recognizer = cv2.face.LBPHFaceRecognizer_create()

    for folder in os.listdir(dataset_path):
        folder_path = os.path.join(dataset_path, folder)

        if not os.path.isdir(folder_path):
            continue

        try:
            student_id = int(folder.split("_")[0])
        except:
            print(f"Skipping folder {folder}")
            continue

        for image_name in os.listdir(folder_path):
            image_path = os.path.join(folder_path, image_name)

            img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue

            faces.append(img)
            ids.append(student_id)

    if len(faces) == 0:
        raise Exception("No training images found!")

    ids = np.array(ids)

    if not os.path.exists("trainer"):
        os.makedirs("trainer")

    recognizer.train(faces, ids)
    recognizer.save("trainer/trainer.yml")

    print("✅ Model Trained Successfully")