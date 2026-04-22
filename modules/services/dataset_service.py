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

    def save_batch(self, examples):
        self.repo.insert_batch(examples)

        # actualizar cache en memoria
        for ex in examples:
            self.data.append(ex['landmarks'])
            self.letters.append(ex['letter'])
