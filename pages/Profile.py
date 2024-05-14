import streamlit as st
from streamlit_navigation_bar import st_navbar

st.set_page_config(
    page_title = "고민모니",
    page_icon = "./images/logo.png",
    initial_sidebar_state="collapsed",
    show_sidebar = True,
    show_menu = False
)

page = st_navbar(["고민모니?", "대시보드", "상세보기",  "내프로필"], selected="내프로필")

if page == "상세보기":
    st.switch_page("pages/History.py")

if page == "대시보드":
    st.switch_page("pages/Home.py")

if page == "고민모니?":
    st.switch_page("pages/About.py")

####################################################################################
st.write("프로필 변경.")