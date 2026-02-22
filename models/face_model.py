import cv2
import os
import numpy as np
from PIL import Image


class FaceModel:

    def __init__(self, dataset_path="dataset", trainer_path="trainer"):
        self.dataset_path = dataset_path
        self.trainer_path = trainer_path
        self.model_path = os.path.join(trainer_path, "trainer.yml")

        if not os.path.exists(trainer_path):
            os.makedirs(trainer_path)

        self.recognizer = cv2.face.LBPHFaceRecognizer_create()

    # ---------------- TRAIN MODEL ----------------
    def train(self):

        faces = []
        labels = []
        label_map = {}
        current_label = 0

        for person_name in os.listdir(self.dataset_path):
            person_path = os.path.join(self.dataset_path, person_name)

            if not os.path.isdir(person_path):
                continue

            label_map[current_label] = person_name

            for image_name in os.listdir(person_path):
                image_path = os.path.join(person_path, image_name)

                img = Image.open(image_path).convert("L")
                img_numpy = np.array(img, "uint8")

                faces.append(img_numpy)
                labels.append(current_label)

            current_label += 1

        if len(faces) == 0:
            raise Exception("No dataset found for training.")

        self.recognizer.train(faces, np.array(labels))
        self.recognizer.save(self.model_path)

        print("Model Training Completed Successfully")

        return label_map

    # ---------------- LOAD MODEL ----------------
    def load(self):
        if not os.path.exists(self.model_path):
            raise Exception("Model not trained yet.")
        self.recognizer.read(self.model_path)

    # ---------------- RECOGNIZE FACE ----------------
    def recognize(self, gray_face):

        id, confidence = self.recognizer.predict(gray_face)

        return id, confidence