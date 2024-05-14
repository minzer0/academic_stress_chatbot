import streamlit as st


def menu():
    # Show a navigation menu
    st.sidebar.page_link("pages/About.py", label="고민모니 소개")
    st.sidebar.page_link("pages/Home.py", label="홈 화면")
    st.sidebar.page_link("pages/Chatbot.py", label="챗봇")
    st.sidebar.page_link("pages/Result.py", label="결과")
    st.sidebar.page_link("pages/History.py", label="이전 기록")
    st.sidebar.page_link("app.py", label="로그아웃")