import streamlit as st
import numpy as np
import altair as alt
import pandas as pd
from menu import menu
from datetime import datetime
from st_supabase_connection import SupabaseConnection

from dummy_data import df_sorted
from result_dictionary import stressor_icons
from result_dictionary import symptoms_icons
from result_dictionary import coping_icons

# from Result import stressor, stressor_icon, symptom, symptom_icon, coping, coping_icon

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


st_supabase_client = st.connection("supabase",type=SupabaseConnection)
user_id = st.session_state["user_id"]
user_name = st.session_state["user_metadata"]["user_name"]


data = st_supabase_client.table("history").select("*").execute()
df = pd.DataFrame(data.data)
current_date = datetime.now()

filtered_df = df[(df['user_name'] == user_name) & 
                 (df['user_id'] == user_id) &
                 (df['date'] == str(current_date.year) + '-' + str(current_date.month) + '-' + str(current_date.day))]
filtered_df.reset_index(drop=True, inplace=True)

history_df = df[(df['user_name'] == user_name) & 
                (df['user_id'] == user_id) &
                (df['date'] != str(current_date.year) + '-' + str(current_date.month) + '-' + str(current_date.day))]

history_df_de = history_df.sort_values(by='date', ascending=False)
history_df_de.reset_index(drop=True, inplace=True)

########################################################################################
st.title(f"{user_name}님의 학업 스트레스 지수")

if len(history_df) == 0:
    st.image('./images/nulldata.png')
else:
    with st.container(border=True):        
        # 사용자 학업 스트레스 점수와 해당 구간의 사람 수 표시
        st.write(f"지난 번 {user_name}님의 점수는 **{history_df_de.loc[0, 'average_score']:.2f}**로, 전체 사용자 중 상위 **{history_df_de.loc[0, 'percentile']:2f}**%에요.")

        # 데이터 생성
        np.random.seed = 42  # 재현성을 위해 랜덤 시드 설정
        n_samples = 100  # 샘플 수

        # 정규분포 데이터 생성
        data = np.random.normal(3.773399014778325, 0.9273521676028207, n_samples)
        df = pd.DataFrame(data, columns=['score'])

        # 히스토그램 생성
        base_histogram = (
            alt.Chart(df)
            .mark_bar()
            .encode(
                x=alt.X("score:Q", bin=alt.Bin(extent=[1.0, 5.0], step=0.5)),  # 5점 간격으로 분할
                y="count()",
                color=alt.value("lightgray")
            )
        )

        # 특정 영역 강조
        highlight = (
            alt.Chart(df[df['score'].between(history_df_de.loc[0, 'average_score']-0.1, history_df_de.loc[0, 'average_score']+0.1)])  # 점수 기준 +/-5 범위
            .mark_bar(color='#ffc8ce')  # 강조 색상 설정
            .encode(
                x=alt.X("score:Q", bin=alt.Bin(extent=[1.0, 5.0], step=0.5)),
                y="count()",
            )
        )

        # 히스토그램과 강조 영역 결합
        final_chart = base_histogram + highlight

        # 차트 렌더링
        st.altair_chart(final_chart, use_container_width=True)

    summary = history_df_de.loc[0, 'summary']
    summary_list = [sentence.strip() for sentence in summary.split('\n') if sentence]

    with st.container():
        col1, col2, col3 = st.columns(3)

        # 스트레스 원인
        with col1:
            st.subheader("스트레스 원인")
            stressor = summary_list[0].split(':')[0].strip()
            stressor_explain = summary_list[0].split(':')[1].strip() 
            stressor_icon = stressor_icons.get(stressor, '👌')
            st.write(f"{stressor_icon} {stressor}")
            st.write(f"{stressor_explain}")

        # 스트레스 증상
        with col2:
            st.subheader("스트레스 증상")
            symptom = summary_list[1].split(':')[0].strip()
            symptom_explain = summary_list[1].split(':')[1].strip() 
            symptom_icon = symptoms_icons.get(symptom, '👌')
            st.write(f"{symptom_icon} {symptom}")
            st.write(f"{symptom_explain}")

        # 스트레스 대처 전략
        with col3:
            st.subheader("스트레스 대처 전략")
            coping = summary_list[2].split(':')[0].strip()
            coping_explain = summary_list[2].split(':')[1].strip() 
            coping_icon = coping_icons.get(coping, '👌')
            st.write(f"{coping_icon} {coping}")
            st.write(f"{coping_explain}")

st.write("#")
st.write("#")

if st.button(":left_speech_bubble:   모니와 대화하며 \n **새로운 학업 스트레스 측정**하기",
            use_container_width=True, ):
    st.switch_page("pages/Chatbot.py")
if st.button(":bar_chart:    이전 기록 확인하기",
             use_container_width=True):
    st.switch_page("pages/History.py")

menu()