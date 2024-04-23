import os
import streamlit as st

st.set_page_config(
    page_title = "고민모니",
    page_icon = "./images/logo.png"
)


st.image('./images/app_img.png')


# 텍스트 추가
st.markdown(
    "<div style='font-family: \"Nanum Gothic\"; text-align: center;'>"
    "당신의 학업 고민을 들려주세요!<br>학업 스트레스 모니터링 챗봇"
    "</div>",
    unsafe_allow_html=True,
)

# 큰 타이틀 추가
st.markdown(
    "<div style='font-family: \"Nanum Gothic\"; text-align: center; font-size: 36px; font-weight: bold;'>"
    "고민모니"
    "</div>",
    unsafe_allow_html=True,
)

# 아래쪽에 여러 줄의 공백
st.write("#")

col1, col2, col3 , col4, col5 = st.columns(5)

with col3 :
    if st.button("로그인"):
        st.switch_page("pages/Login.py")
    if st.button("회원가입"):
        st.switch_page("pages/Signup.py")
    # st.image('./images/HAI_logo.png', width = 100)