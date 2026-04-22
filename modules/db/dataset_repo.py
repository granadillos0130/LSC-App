from modules.db.db import supabase

class DatabaseRepository:

    def get_all(self, batch_size=1000):
        start = 0
        all_data = []

        try:
            while True:
                response = supabase.table("training_data")\
                    .select("letter, landmarks")\
                    .range(start, start + batch_size - 1)\
                    .execute()

                data = response.data
                if not data:
                    break

                all_data.extend(data)
                start += batch_size

            return all_data
        except Exception as e:
            print(f"Error al obtener los datos: {e}")
            return []
    
    def insert_batch(self, examples, batch_size=500):
        try:
            for i in range(0, len(examples), batch_size):
                batch = examples[i:i + batch_size]
                supabase.table("training_data").insert(batch).execute()
        except Exception as e:
            print(f"Error insertando datos: {e}")    