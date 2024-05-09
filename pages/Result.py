import streamlit as st
import pandas as pd
from datetime import datetime
from st_supabase_connection import SupabaseConnection
import altair as alt
import numpy as np

from function.result_dictionary import stressor_icons
from function.result_dictionary import symptoms_icons
from function.result_dictionary import coping_icons
from function.menu import menu

# from backend import average_score, percentile, summary, overall_summary
from dummy_data import df_sorted

#######################################################################################
# SETUP

st.set_page_config(
    page_title = "고민모니",
    page_icon = "./images/logo.png"
)

# .streamlit/style.css 파일 열기
with open("./.streamlit/style.css") as css:
    # CSS 파일을 읽어와서 스타일 적용
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)


st_supabase_client = st.connection("supabase",type=SupabaseConnection)

if "user_id" not in st.session_state:
    st.error("로그인이 필요합니다.")
    if st.button("로그인하러 가기"):
        st.switch_page("pages/Login.py")
    st.stop()

user_id = st.session_state["user_id"]
user_name = st.session_state["user_metadata"]["user_name"]


data = st_supabase_client.table("history").select("*").execute()
df = pd.DataFrame(data.data)
current_date = datetime.now()

filtered_df = df[(df['user_name'] == user_name) & 
                 (df['user_id'] == user_id) &
                 (df['date'] == str(current_date.year) + '-' + str(current_date.month) + '-' + str(current_date.day))]
filtered_df.reset_index(drop=True, inplace=True)

average_score = filtered_df.loc[0, 'average_score']
percentile = filtered_df.loc[0, 'percentile']
summary = filtered_df.loc[0, 'summary']
overall_summary = filtered_df.loc[0, 'overall_summary']

history_df = df[(df['user_name'] == user_name) & 
                (df['user_id'] == user_id) &
                (df['date'] != str(current_date.year) + '-' + str(current_date.month) + '-' + str(current_date.day))]

history_df_as = history_df.sort_values(by='date', ascending=True)
history_df_as.rename(columns={"date": "날짜", "average_score": "스트레스 점수"}, inplace=True)
history_df_as.reset_index(drop=True, inplace=True)

today = datetime.now().strftime("%Y-%m-%d")
new_data = pd.DataFrame({'날짜': [today], '스트레스 점수': [average_score]})
history_df_as = pd.concat([history_df_as, new_data], ignore_index=True)
history_df_as.reset_index(drop=True, inplace=True)

########################################################################################
if len(filtered_df) == 0:
    st.image('./images/nulldata3.png')
    if st.button("모니와 대화하러 가기"):
        st.switch_page("pages/Chatbot.py")
    st.stop()

else:
# 메인 헤더
    # 평탄화된 리스트 생성
    summary_list = [sentence.strip() for sentence in summary.split('\n') if sentence]
    st.header("학업 스트레스 검사 결과")
    # 사용자 학업 스트레스 점수와 해당 구간의 사람 수 표시
    st.write(f"{user_name}님의 점수는 {average_score: .2f}로, 전체 사용자 중 상위 **{percentile}**%에요.")

    with st.container(border=True):        
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
                alt.Chart(df[df['score'].between(average_score-0.1, average_score+0.1)])  # 점수 기준 +/-5 범위
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


    # 스트레스 원인 정보
    st.markdown("### 스트레스 원인")
    stressor = summary_list[0].split(':')[0].strip()
    stressor_explain = summary_list[0].split(':')[1].strip() 
    stressor_icon = stressor_icons.get(stressor, '👌')
    st.write(f"{stressor_icon} {stressor}")
    st.write(f"{stressor_explain}")

# 스트레스 증상
    st.markdown("### 스트레스 증상")
    symptom = summary_list[1].split(':')[0].strip()
    symptom_explain = summary_list[1].split(':')[1].strip() 
    symptom_icon = symptoms_icons.get(symptom, '👌')
    st.write(f"{symptom_icon} {symptom}")
    st.write(f"{symptom_explain}")

    # 스트레스 대처 전략 정보
    st.markdown("### 스트레스 대처 전략")
    coping = summary_list[2].split(':')[0].strip()
    coping_explain = summary_list[2].split(':')[1].strip() 
    coping_icon = coping_icons.get(coping, '👌')
    st.write(f"{coping_icon} {coping}")
    st.write(f"{coping_explain}")


    st.write("#")

    st.subheader("학업 스트레스 점수 추이")

    # 라인 차트 시각화
    if len(history_df_as) == 1:
        st.scatter_chart(history_df_as, x="날짜", y="스트레스 점수", color='#ffc8ce')
    else:
        st.line_chart(history_df_as, x="날짜", y="스트레스 점수", color='#ffc8ce')

col1, col2, col3 = st.columns(3)
with col2:
    if st.button(":bar_chart:    이전 기록 확인하기",
            use_container_width=True):
        st.switch_page("pages/History.py")
    if st.button("🏠   홈 화면으로 돌아가기",
            use_container_width=True, ):
        st.switch_page("pages/Chatbot.py")

menu()
