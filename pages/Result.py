import streamlit as st
import pandas as pd
from datetime import datetime
from st_supabase_connection import SupabaseConnection
import altair as alt
import numpy as np
from scipy.stats import norm
import plotly.graph_objects as go

from function.result_dictionary import stressor_icons
from function.result_dictionary import symptoms_icons
from function.result_dictionary import coping_icons
from function.menu import menu


#######################################################################################
# SETUP

# .streamlit/style.css 파일 열기
with open("./.streamlit/style.css") as css:
    # CSS 파일을 읽어와서 스타일 적용
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)


st_supabase_client = st.connection("supabase",type=SupabaseConnection)

if "user_id" not in st.session_state:
    st.error("로그인이 필요합니다.")
    if st.button("로그인하러 가기"):
        st.switch_page("pages/Login.py")
    menu()
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

if len(filtered_df) == 0:
    st.image('./images/nulldata3.png')
    if st.button("모니와 대화하러 가기"):
        st.switch_page("pages/Chatbot.py")

else: 

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

    range_labels = ["고민이모니", "이정도는OK", "인생이힘드니", "조금지쳐", "폭발직전"]
########################################################################################


    score_ranges = [1.94, 3.09, 3.72, 4.39, 5.0]

    def score_classification(score):
        for idx, upper_bound in enumerate(score_ranges):
            if score <= upper_bound:
                return idx
    
    st.markdown("# 학업 스트레스 측정 결과")          
    with st.container(border=True):
        st.subheader("학업 스트레스 점수 확인")
        # 평탄화된 리스트 생성
        summary_list = [sentence.strip() for sentence in summary.split('\n') if sentence]
        # 사용자 학업 스트레스 점수와 해당 구간의 사람 수 표시
        st.write(f"{user_name}님의 점수는 {average_score: .2f}/5.0로, 100명 중 **{percentile}**째로 스트레스가 많아요.")

        # 데이터 생성
        np.random.seed = 42  # 재현성을 위해 랜덤 시드 설정
        dummy_scores = np.random.normal(3.773399014778325, 0.9273521676028207, 1000)
        mu, std = np.mean(dummy_scores), np.std(dummy_scores)  # 평균과 표준편차 계산

        # PDF 그래프 생성
        x = np.linspace(min(dummy_scores), max(dummy_scores), 100)
        y = norm.pdf(x, mu, std)  # 확률밀도함수

        # Plotly 그래프 생성
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='확률밀도함수', line=dict(color='grey')))

        # 사용자 점수 주변 영역 강조
        score_min = average_score - 0.2
        score_max = average_score + 0.2
        x_fill = np.linspace(score_min, score_max, 100)
        y_fill = norm.pdf(x_fill, mu, std)


        stress_color = ['#277da1', '#90be6d', '#f9c74f', '#f8961e', '#f94144']  # 각 구간에 대해 다른 색상 지정

        part_color = stress_color[score_classification(average_score)]
        fig.add_trace(go.Scatter(x=x_fill, y=y_fill, fill='tozeroy', mode='none', name='당신의 스트레스 수치',
                                fillcolor=part_color, opacity=0.3))

        fig.update_layout(
                        xaxis_title='학업 스트레스 점수',
                        yaxis_title='확률밀도함수',
                        legend_title='범례')
        st.plotly_chart(fig, use_container_width=True)

        # st.subheader("학업 스트레스 점수 추이")
        
        # # 데이터프레임을 Altair에 맞게 변환
        # base_chart = alt.Chart(history_df_as).mark_line(point=True).encode(
        #     x='date:T',
        #     y=alt.Y('average_score:Q', scale=alt.Scale(domain=[0.5, 5.5]), title="학업 스트레스 수치"),
        #     color=alt.value("#000000")
        # )

        # # 구간별 척도 가로선 추가
        # rule_data = pd.DataFrame({
        #     '학업 스트레스 단계': score_ranges,
        #     '구간': range_labels, 
        #     '색상': ['#277da1', '#90be6d', '#f9c74f', '#f8961e', '#f94144']  # 각 구간에 대해 다른 색상 지정

        # })

        # rule_chart = alt.Chart(rule_data).mark_rule(strokeDash=[5, 3]).encode(
        #     y='학업 스트레스 단계:Q',
        #     color=alt.Color('색상:N', scale=None)
        # )

        # final_chart = base_chart + rule_chart 

        # st.altair_chart(final_chart, use_container_width=True)
        # st.image('./images/스트레스 수치/스트레스5단계.png')
    
    # 스트레스 원인 정보
    stressor = summary_list[0].split(':')[0].strip()
    stressor_explain = summary_list[0].split(':')[1].strip() 
    stressor_icon = stressor_icons.get(stressor, '👌')
    st.markdown(f"### 스트레스 원인: {stressor_icon} {stressor}")
    # st.write(f"{stressor_icon} {stressor}")
    st.write(f"{stressor_explain}")

# 스트레스 증상
    symptom = summary_list[1].split(':')[0].strip()
    symptom_explain = summary_list[1].split(':')[1].strip() 
    symptom_icon = symptoms_icons.get(symptom, '👌')
    st.markdown("### 스트레스 증상")
    st.write(f"{symptom_icon} {symptom}")
    st.write(f"{symptom_explain}")

    # 스트레스 대처 전략 정보
    coping = summary_list[2].split(':')[0].strip()
    coping_explain = summary_list[2].split(':')[1].strip() 
    coping_icon = coping_icons.get(coping, '👌')
    st.markdown("### 스트레스 대처 전략")
    st.write(f"{coping_icon} {coping}")
    st.write(f"{coping_explain}")


    st.write("#")




    col1, col2, col3 = st.columns(3)
    with col2:
        if st.button(":bar_chart:    이전 기록 확인하기",
                use_container_width=True):
            st.switch_page("pages/History.py")
        if st.button("🏠   홈 화면으로 돌아가기",
                use_container_width=True, ):
            st.switch_page("pages/Home.py")

menu()
