from st_supabase_connection import SupabaseConnection
from datetime import datetime
import pandas as pd

user_id = st.session_state["user_id"]
user_name = st.session_state["user_metadata"]["user_name"]
current_date = datetime.now().isoformat()

current_year = int(current_date[:4])
current_month = int(current_date[5:7])
current_day = int(current_date[8:10])

# Filter the DataFrame based on the conditions
filtered_df = df[(st_supabase_client.table("chat")['user_name'] == user_name) &
                 (st_supabase_client.table("chat")['user_id'] == user_id) &
                 (st_supabase_client.table("chat")['created_at'].dt.year == current_year) &
                 (st_supabase_client.table("chat")['created_at'].dt.month == current_month) &
                 (st_supabase_client.table("chat")['created_at'].dt.day == current_day)]

