import numpy as np
import json
import os

class SignClassifier:
    def __init__(self, data_path='data/dataset.json'):
        self.data_path = data_path
        self.dataset = []
        self.labels = []
        self.load_dataset()

    def load_dataset(self):
        if os.path.exists(self.data_path):
            with open(self.data_path, 'r') as f:
                data = json.load(f)
                self.dataset = [item['landmarks'] for item in data]
                self.labels = [item['label'] for item in data]
                print(f"Dataset cargado: {len(self.labels)} ejemplos")
        else:
            print("No hay dataset aun hay que entrenar el modelo")

    def save_example(self, landmarks, label):
        data = []
        if os.path.exists(self.data_path):
            with open(self.data_path, 'r') as f:
                data = json.load(f)
        
        data.append({'label': label, 'landmarks': landmarks})

        with open(self.data_path, 'w') as f:
            json.dump(data,f)

        self.dataset.append(landmarks)
        self.labels.append(label)
        print(f"Ejemplo guardado: {label} — Total: {len(self.labels)}")

    def predict(self, landmarks, k=5):
        if len(self.dataset) <k:
            return None, 0.0
        
        distances = []
        for i, sample in enumerate(self.dataset):
            dist = np.linalg.norm(np.array(landmarks)- np.array(sample))
            distances.append((dist, self.labels[i]))

        distances.sort(key=lambda x: x[0])
        top_k = distances[:k]

        votes = {}
        for dist, label in top_k:
            votes[label] = votes.get(label,0) + 1

        beast_label = max(votes, key=votes.get)
        confidence = votes[beast_label] / k

        return beast_label, confidence 