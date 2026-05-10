from .db import supabase

class DatabaseRepository:

    def get_all(self):
        res = supabase.table("training_data").select("*").execute()
        return res.data
    
    def save(self, item):
        supabase.table("training_data").insert(item).execute()

    def save_batch(self, examples, batch_size=30):
        try:
        # Insertar en lotes para evitar payloads demasiado grandes
            for i in range(0, len(examples), batch_size):
                batch = examples[i:i + batch_size]
                supabase.table("training_data").insert(batch).execute()
        except Exception as e:
            print(f"Error insertando datos: {e}")    