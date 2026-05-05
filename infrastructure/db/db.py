from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

url=os.getenv("SUPABASE_URL")
key=os.getenv("SUPABASE_KEY")

supabase = create_client(url, key)

try:
    response = supabase.table("training_data").select("*").limit(1).execute()

    if response.data is not None:
        print("Conectado correctamente a la db.")

except Exception as e:
    print("Error de conexion a la db.", str(e))
