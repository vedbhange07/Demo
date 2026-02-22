import cv2
import os
import numpy as np
from PIL  import Image

dataset_path = "dataset"
trainer_path = "trainer"

if not os.path.exists(trainer_path):
    os.makedirs(trainer_path)

recognizer = cv2.face.LBPHFaceRecognizer_create()

faces = []
labels = []
label_map = {}
current_label = 0

for person_name in os.listdir(dataset_path):
    person_path = os.path.join(dataset_path, person_name)

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

recognizer.train(faces, np.array(labels))
recognizer.save("trainer/trainer.yml")

print("Training Complete! Model saved in trainer/trainer.yml")