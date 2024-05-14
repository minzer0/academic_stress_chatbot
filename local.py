import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm
from wordcloud import WordCloud
import matplotlib.font_manager as fm
import plotly.graph_objects as go
from streamlit_navigation_bar import st_navbar

score_ranges = [1.94, 3.09, 3.72, 4.39, 5.0]

styles = {
    "nav" : {
        "font-family": "Gowun Batang",
    },
}


options = {
    "show_menu": False,
    "show_sidebar": True,
}


page = st_navbar(["고민모니?", "대시보드", "상세보기", "내프로필"],
                 options=options,
                 )
st.write(page)

# .streamlit/style.css 파일 열기
with open("./.streamlit/style.css", 'rt', encoding='UTF8') as css:
    # CSS 파일을 읽어와서 스타일 적용
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)


st.title("결과 분석 중입니다...🔍\n 쪼꼼만 기다려주이소~~>< \n 오래 걸려도 이해해 줄 수 있지예~~?❤️❤️❤️")


def score_classification(score):
    for idx, upper_bound in enumerate(score_ranges):
        if score <= upper_bound:
            return idx
        
# 스트림릿 앱 제목
st.title('학업 스트레스 측정')

# 사용자 입력: 학업 스트레스 점수
user_score = st.number_input('당신의 학업 스트레스 점수를 입력하세요:', min_value=0, max_value=5, value=5, step=1)


# 예시 데이터 생성 (임시로 정규 분포 사용)
np.random.seed(0)
dummy_scores = np.random.normal(3.773399014778325, 0.9273521676028207, 1000)
mu, std = np.mean(dummy_scores), np.std(dummy_scores)  # 평균과 표준편차 계산

# 사용자 점수의 위치를 백분위로 계산
percentile = norm.cdf(user_score, mu, std) * 100
st.write(f'당신의 학업 스트레스 점수는 상위 {100-percentile:.2f}%에 위치합니다.')

# PDF 그래프 생성
x = np.linspace(min(dummy_scores), max(dummy_scores), 100)
y = norm.pdf(x, mu, std)  # 확률밀도함수

# Plotly 그래프 생성
fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='확률밀도함수', line=dict(color='grey')))

# 사용자 점수 주변 영역 강조
score_min = user_score - 0.2
score_max = user_score + 0.2
x_fill = np.linspace(score_min, score_max, 100)
y_fill = norm.pdf(x_fill, mu, std)


stress_color = ['#277da1', '#90be6d', '#f9c74f', '#f8961e', '#f94144']  # 각 구간에 대해 다른 색상 지정

part_color = stress_color[score_classification(user_score)]
fig.add_trace(go.Scatter(x=x_fill, y=y_fill, fill='tozeroy', mode='none', name='당신의 스트레스 수치',
                          fillcolor=part_color, opacity=0.3))

fig.update_layout(xaxis_title='학업 스트레스 점수',
                  yaxis_title='Probability Density',
                  legend_title='범례')

st.plotly_chart(fig, use_container_width=True)


