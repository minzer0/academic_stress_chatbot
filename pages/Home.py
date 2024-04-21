import streamlit as st

if "user_metadata" not in st.session_state:
    st.error("로그인이 필요합니다.")
    if st.button("로그인하러 가기"):
        st.switch_page("pages/Login.py")
    st.stop()

st.title(f"{st.session_state['user_metadata']['user_name'][1:]}님의 학업 스트레스 지수")

with st.container(border=True):
    st.markdown("또래 100명 중..")
    
if st.button("모니와 대화하며 새로운 학업 스트레스 측정하기"):
    st.switch_page("pages/Chatbot.py")
if st.button("이전 기록 확인하기"):
    st.switch_page("pages/History.py")
