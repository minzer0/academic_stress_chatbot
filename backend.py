from st_supabase_connection import SupabaseConnection
from datetime import datetime
import streamlit as st
import pandas as pd

st_supabase_client = st.connection("supabase",type=SupabaseConnection)

user_id = st.session_state["user_id"]
user_name = st.session_state["user_metadata"]["user_name"]
current_date = datetime.now()

data = st_supabase_client.table("chat").select("*").execute()
df = pd.DataFrame(data.data)
df['created_at'] = pd.to_datetime(df['created_at'])

filtered_df = df[(df['user_name'] == user_name) & 
                 (df['user_id'] == user_id) &
                 (df['created_at'].dt.year == current_date.year) &
                 (df['created_at'].dt.month == current_date.month) &
                 (df['created_at'].dt.day == current_date.day)]