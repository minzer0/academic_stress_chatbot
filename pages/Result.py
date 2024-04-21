import streamlit as st

st.title("결과")
if st.button("이전 결과 확인하기"):
    st.switch_page("pages/History.py")