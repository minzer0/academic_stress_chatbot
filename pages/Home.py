import streamlit as st
import numpy as np
import altair as alt
import pandas as pd
from menu import menu

from dummy_data import df_sorted
from result_dictionary import stressor_icons
from result_dictionary import symptoms_icons
from result_dictionary import coping_icons

########################################################################################
# SETUP 

st.set_page_config(
    page_title = "고민모니",
    page_icon = "./images/logo.png"
)

# .streamlit/style.css 파일 열기
with open("./.streamlit/style.css") as css:
    # CSS 파일을 읽어와서 스타일 적용
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)

if "user_metadata" not in st.session_state:
    st.error("로그인이 필요합니다.")
    if st.button("로그인하러 가기"):
        st.switch_page("pages/Login.py")
    st.stop()

st.title(f"{st.session_state['user_metadata']['user_name'][1:]}님의 학업 스트레스 지수")

########################################################################################

with st.container(border=True):
    # 사용자 학업 스트레스 점수
    user_score = 85
    
    # 사용자 학업 스트레스 점수와 해당 구간의 사람 수 표시
    st.write(f"지난 번 {st.session_state['user_metadata']['user_name'][1:]}님의 점수는 **{user_score}**로, 또래 100명 중 **70**등이에요.")
    st.write("**:blue[파란색]**: 나와 비슷한 점수(+/-5)를 가진 사람들 ")

    # 데이터 생성
    np.random.seed = 42  # 재현성을 위해 랜덤 시드 설정
    mean = 70  # 평균
    std = 10  # 표준편차
    n_samples = 1000  # 샘플 수

    # 정규분포 데이터 생성
    data = np.random.normal(mean, std, n_samples)
    df = pd.DataFrame(data, columns=['score'])

    # 히스토그램 생성
    base_histogram = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X("score:Q", bin=alt.Bin(extent=[0, 100], step=5)),  # 5점 간격으로 분할
            y="count()",
            color=alt.value("lightgray")
        )
    )

    # 특정 영역 강조
    highlight = (
        alt.Chart(df[df['score'].between(user_score-5, user_score+5)])  # 점수 기준 +/-5 범위
        .mark_bar(color='blue')  # 강조 색상 설정
        .encode(
            x=alt.X("score:Q", bin=alt.Bin(extent=[0, 100], step=5)),
            y="count()",
        )
    )

    # 히스토그램과 강조 영역 결합
    final_chart = base_histogram + highlight

    # 차트 렌더링
    st.altair_chart(final_chart, use_container_width=True)



with st.container():
    col1, col2, col3 = st.columns(3)

    # 스트레스 원인
    with col1:
        st.subheader("스트레스 원인")
        st.write(f"- {df_sorted.loc[1, '스트레스 원인']} {stressor_icons.get(df_sorted.loc[1, '스트레스 원인'], '👌')}")

    # 스트레스 증상
    with col2:
        st.subheader("스트레스 증상")
        st.write(f"- {df_sorted.loc[0, '스트레스 증상']} {symptoms_icons.get(df_sorted.loc[0, '스트레스 증상'], '👌')}")
        st.write(f"- {df_sorted.loc[1, '스트레스 증상']} {symptoms_icons.get(df_sorted.loc[1, '스트레스 증상'], '👌')}")
        st.write(f"- {df_sorted.loc[2, '스트레스 증상']} {symptoms_icons.get(df_sorted.loc[2, '스트레스 증상'], '👌')}")
        
    # 스트레스 대처 전략
    with col3:
        st.subheader("스트레스 대처 전략")
        st.write(f"- {df_sorted.loc[1, '스트레스 대처 전략']} {coping_icons.get(df_sorted.loc[1, '스트레스 대처 전략'], '👌')}")

st.write("#")
st.write("#")

if st.button(":left_speech_bubble:   모니와 대화하며 \n **새로운 학업 스트레스 측정**하기",
            use_container_width=True, ):
    st.switch_page("pages/Chatbot.py")
if st.button(":bar_chart:    이전 기록 확인하기",
             use_container_width=True):
    st.switch_page("pages/History.py")

menu()