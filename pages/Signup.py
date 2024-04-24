import streamlit as st
from st_supabase_connection import SupabaseConnection

########################################################################################
# SETUP

st.set_page_config(
    page_title = "고민모니",
    page_icon = "./images/logo.png"
)

# .streamlit/style.css 파일 열기
with open("./.streamlit/style.css") as css:
    # CSS 파일을 읽어와서 스타일 적용
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)

########################################################################################


st_supabase_client = st.connection("supabase", type=SupabaseConnection)


with st.container(border=True):
    st.markdown("#### 회원가입")
    
    user_name = st.text_input("이름", key="name_signup")
    email = st.text_input("이메일 주소", key="email_signup")
    password = st.text_input("비밀번호", type="password", key="password_signup")           
    
    if st.button("회원가입"):
        try:
            st_supabase_client.auth.sign_up({
                "email": email, 
                "password": password,
                "options": {
                    "data": {
                        "user_name": user_name,
                    }
                }
            })
                            
        except Exception as e:
            st.error("회원가입 실패")
            
        if email and password:
            try:
                supabase_response = st_supabase_client.auth.sign_in_with_password({
                    "email": email, 
                    "password": password,
                })
                
                if supabase_response is not None:
                
                    if "user_id" not in st.session_state:
                        st.session_state["user_id"] = supabase_response.user.id
                    if "user_metadata" not in st.session_state:
                        st.session_state["user_metadata"] = supabase_response.user.user_metadata
                        
                    st.switch_page("pages/Home.py")
            
            except Exception as e:
                st.error("로그인 실패")
                
col1, col2, col3 = st.columns(3)
with col2:
    if st.button("⬅️     시작 화면으로 돌아가기", use_container_width=True):
        st.switch_page("app.py")

# 회색 배경에 작은 글씨로 중앙 정렬된 캡션 추가
st.write("#")

st.markdown(
    "<div style='text-align: center; font-size: small;'>"
    "👯 본 앱은 서울과학기술대학교 인간중심인공지능 연구실<br>유박사 팀에서 개발한 학업 스트레스 측정 챗봇입니다 👯"
    "</div>",
    unsafe_allow_html=True
)