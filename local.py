import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm
from wordcloud import WordCloud
import matplotlib.font_manager as fm
import plotly.graph_objects as go
from streamlit_navigation_bar import st_navbar
import time

score_ranges = [1.94, 3.09, 3.72, 4.39, 5.0]


# .streamlit/style.css 파일 열기
with open("./.streamlit/style.css", 'rt', encoding='UTF8') as css:
    # CSS 파일을 읽어와서 스타일 적용
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)


st.title("결과 분석 중입니다...🔍\n")

# 메시지를 담고 있는 리스트
waiting_list = ["팀 유박사는 유다나 박민영 사랑해라는 뜻입니다 ❤️", "고민모니라는 이름은 ChatGPT가 지어줬습니다", 
                "상상관 4층에는 곱등이가 산다는 소문이 있습니다", "인공지능응용학과 만세! 최고!"]

# 스피너와 함께 메시지 표시

# 메시지를 담고 있는 리스트
waiting_list = ["팀 유박사는 유다나 박민영 사랑해라는 뜻입니다 ❤️", "고민모니라는 이름은 ChatGPT가 지어줬습니다 😎", 
                "상상관 4층에는 곱등이가 산다는 소문이 있습니다 😮", "인공지능응용학과 만세! 최고! 😍",
                "유박사 팀은 이번 여름에 학사 졸업합니다 🎉"]
def spinner_text(i):
    message_ui = f"<div style='text-align: center; font-size: 20px; font-weight: bold;'> {waiting_list[i]} </div>"
    message_holder.markdown(
        message_ui,
        unsafe_allow_html=True,
    )        
    time.sleep(1) 
# 스피너와 함께 메시지 표시
with st.spinner('딱 10초만 기다려주세요!'):
    # 메시지를 동적으로 업데이트하기 위한 임시 위젯 생성
    message_holder = st.empty()
    message_holder.markdown("#")
    message_holder.markdown("#")
    spinner_text(0)

spinner_text(1)
spinner_text(2)