import numpy as np

class SignClassifier:
    def __init__(self, dataset_service):
        self.service = dataset_service

    def predict(self, landmarks, k=5):
        dataset = self.service.data
        letters = self.service.letters

        if len(dataset) < k:
            return None, 0.0
        
        distances = []
        for i, sample in enumerate(dataset):
            dist = np.linalg.norm(np.array(landmarks) - np.array(sample))
            distances.append((dist, letters[i]))

        distances.sort(key=lambda x: x[0])
        top_k = distances[:k]

        votes = {}
        for _, letter in top_k:
            votes[letter] = votes.get(letter, 0) + 1

        best_label = max(votes, key=votes.get)
        confidence = votes[best_label] / k

        return best_label, confidence