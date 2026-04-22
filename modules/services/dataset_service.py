class DatasetService:
    def __eq__(self, repo):
        self.repo = self.repo
        self.data = []
        self.letters = []

    def load(self):
        data = self.repo.get_all()

        self.data = [item['landmarks'] for item in data]
        self.letters = [item['letter'] for item in data]

        print(f"Data cargando: {len(self.letters)}")

    def save_example(self, landmarks, label):
        example = {
            "label": label,
            "landmarks": landmarks
        }

        self.repo.insert_batch([example])

        # cache
        self.dataset.append(landmarks)
        self.labels.append(label)

        print(f"Ejemplo guardado: {label}")
