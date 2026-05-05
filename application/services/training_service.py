#Clase encargada de manejar el entremaniento en forma de servicio (batch)

class TrainingService:
    def __init__(self, dataset_service):
        self.dataset_service = dataset_service

    def save_batch(self, batch):
        try:
            self.dataset_service.repo.save_batch(batch)

            for item in batch:
                self.dataset_servie.data.append(item["landmarks"])
                self.dataset_service.letters.append(item["letter"])
        
        except Exception as e:
            print(f"Error al insertar el lote de data: {e}")