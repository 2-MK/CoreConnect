from supabase import create_client

SUPABASE_URL = "https://rogbncdpauuxcclhmlpa.supabase.co"
SUPABASE_KEY = "sb_publishable_Az6nsNkJ9WVsoRz1mRq86g_Jbs25Rt6"

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)