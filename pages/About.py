import streamlit as st
from streamlit_navigation_bar import st_navbar

page = st_navbar(["고민모니?", "대시보드", "상세보기",  "내프로필"], selected="고민모니?")

if page == "상세보기":
    st.switch_page("pages/History.py")

if page == "대시보드":
    st.switch_page("pages/Home.py")

if page == "내프로필":
    st.switch_page("pages/Profile.py")

####################################################################################
st.write("고민모니는 학생들의 학업 스트레스를 개선하기 위해 고안되었어요.")
st.image('./images/HAI_logo.png')