import os
import streamlit as st
from PIL import Image, ImageDraw, ImageFont


st.set_page_config(
    page_title = "고민모니",
    page_icon = "./images/logo.png"
)

st.image('./images/app_img.png')


# .streamlit/style.css 파일 열기
with open("./.streamlit/style.css") as css:
    # CSS 파일을 읽어와서 스타일 적용
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)

                # 스타일이 적용된 Markdown 출력
st.markdown("""
<div style='text-align: center;'>
당신의 학업 고민을 들려주세요!<br>학업 스트레스 모니터링 챗봇
</div>
""", unsafe_allow_html=True)

# 큰 타이틀 추가
st.markdown(
    "<div style='text-align: center; font-size: 36px; font-weight: bold;'>"
    "고민모니"
    "</div>",
    unsafe_allow_html=True,
)

# 아래쪽에 여러 줄의 공백
st.write("#")

col1, col2, col3 , col4, col5 = st.columns(5)

with col3 :
    if st.button("로그인", use_container_width=True):
        st.switch_page("pages/Login.py")
    if st.button("회원가입",use_container_width=True):
        st.switch_page("pages/Signup.py")
    # st.image('./images/HAI_logo.png', width = 100)


# 회색 배경에 작은 글씨로 중앙 정렬된 캡션 추가
st.write("#")

st.markdown(
    "<div style='text-align: center; font-size: small;'>"
    "👯 본 앱은 서울과학기술대학교 인간중심인공지능 연구실<br>유박사 팀에서 개발한 학업 스트레스 측정 챗봇입니다 👯"
    "</div>",
    unsafe_allow_html=True
)