from .db import supabase

class DatabaseRepository:

    def get_all(self):
        res = supabase.table("training_data").select("*").execute()
        return res.data
    
    def save(self, item):
        supabase.table("training_data").insert(item).execute()

    def save_batch(self, examples, batch_size=500):
        try:
            supabase.table("training_data").insert(items).execute()
        except Exception as e:
            print(f"Error insertando datos: {e}")    