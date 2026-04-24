class DatasetService:
    def __init__(self, repo):
        self.repo = repo
        self.data = []
        self.letters = []
        self.load()

    def load(self):
        try:
            data = self.repo.get_all()

            self.data = [item['landmarks'] for item in data]
            self.letters = [item['letter'] for item in data]

            print(f"Data cargando: {len(self.letters)}")
        except Exception as e:
            print(f"Error al cargar la información: {e}")

    def save_example(self, landmarks, letter):
        try:
            example = {
                "letter": letter,
                "landmarks": landmarks
            }

            self.repo.insert_batch([example])

            # cache
            self.data.append(landmarks)
            self.letters.append(letter)

            print(f"Ejemplo guardado: {letter}")
        except Exception as e:
            print(e)

    def save_batch(self, examples):
        try:
            self.repo.insert_batch(examples)

            for ex in examples:
                self.dataset.append(ex["landmarks"])
                self.labels.append(ex["letter"])

            print(f"Lote guardado: {len(examples)} ejemplos")
        except Exception as e:
            print(f"Error al gurdar: {e}")
