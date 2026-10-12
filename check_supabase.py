from core.supabase_client import supabase

try:
    response = supabase.table('insights').select('*').execute()
    print("Insights:", response.data)
except Exception as e:
    print("Error:", e)
