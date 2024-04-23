import streamlit as st
# from pip import SupabaseConnection
from st_supabase_connection import SupabaseConnection


st_supabase_client = st.connection("supabase",type=SupabaseConnection)

with st.container(border=True):
    st.markdown("#### 로그인")
    
    email = st.text_input("이메일 주소", key="email_login")
    password = st.text_input("비밀번호", type="password", key="password_login")
    st.button("로그인")
    
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
    main_button = st.button(label = "⬅️     시작 화면으로 돌아가기")

# 회색 배경에 작은 글씨로 중앙 정렬된 캡션 추가
st.write("#")

st.markdown(
    "<div style='text-align: center; font-size: small;'>"
    "👯 본 앱은 서울과학기술대학교 인간중심인공지능 연구실<br>유박사 팀에서 개발한 학업 스트레스 측정 챗봇입니다 👯"
    "</div>",
    unsafe_allow_html=True
)