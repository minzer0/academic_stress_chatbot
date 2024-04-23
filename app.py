import os
import streamlit as st

st.set_page_config(
    page_title = "고민모니",
    page_icon = "./images/logo.png"
)


st.markdown("당신의 학업 고민을 들려주세요!")
st.markdown("학업 스트레스 모니터링 챗봇")
st.title("고민모니")

if st.button("로그인"):
    st.switch_page("pages/Login.py")
if st.button("회원가입"):
    st.switch_page("pages/Signup.py")