from core.supabase_client import supabase

tables = [
    'users',
    'events',
    'event_participants',
    'alumni_details',
    'placed_students',
    'placement_opportunities',
    'study_materials',
    'insights',
    'fund_management',
    'admin'
]

print("Table row counts:")
for table in tables:
    try:
        # We can fetch count by doing select id with count='exact' but supabase python client might not support it easily
        # Let's just fetch all rows and count
        response = supabase.table(table).select('*').execute()
        print(f"{table}: {len(response.data)}")
    except Exception as e:
        print(f"{table}: Error - {e}")
