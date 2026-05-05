from modules.db.db import supabase

class DatabaseRepository:

    def get_all(self):
        res = supabase.table("training_data").select(*).execute()
        return res.data
    

    def insert_batch(self, examples, batch_size=500):
        try:
            for i in range(0, len(examples), batch_size):
                batch = examples[i:i + batch_size]
                supabase.table("training_data").insert(batch).execute()
        except Exception as e:
            print(f"Error insertando datos: {e}")    