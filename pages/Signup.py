import streamlit as st
from st_supabase_connection import SupabaseConnection


st_supabase_client = st.connection("supabase",type=SupabaseConnection)

with st.container(border=True):
    st.markdown("#### 회원가입")
    
    user_email = st.text_input("이름", key="user_email")
    email = st.text_input("이메일 주소", key="email_signup")
    password = st.text_input("비밀번호", type="password", key="password_signup")           
            
    if st.button("회원가입"):
        try:
            st_supabase_client.auth.sign_up({
                "email": email, 
                "password": password,
                "options": {
                    "data": {
                        "user_email": user_email,
                    }
                }
            })
                            
        except Exception as e:
            st.error("회원가입 실패")