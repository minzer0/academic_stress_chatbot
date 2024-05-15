import streamlit as st
from function.result_dictionary import stressor_icons
from function.result_dictionary import symptoms_icons
from function.result_dictionary import coping_icons
from function.menu import menu

import numpy as np
from scipy.stats import norm

from datetime import datetime
import altair as alt
from st_supabase_connection import SupabaseConnection
import pandas as pd
import plotly.graph_objects as go

########################################################################################
# SETUP

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

history_df = df[(df['user_name'] == user_name) & 
                (df['user_id'] == user_id) &
                (df['date'] != str(current_date.year) + '-' + str(current_date.month) + '-' + str(current_date.day))]

history_df_as = history_df.sort_values(by='date', ascending=True)
history_df_as.rename(columns={"date": "날짜", "average_score": "스트레스 점수"}, inplace=True)
history_df_as.reset_index(drop=True, inplace=True)

history_df_de = history_df.sort_values(by='date', ascending=False)
history_df_de.reset_index(drop=True, inplace=True)
score_ranges = [1.94, 3.09, 3.72, 4.39, 5.0]
range_labels = ["고민이모니", "이정도는OK", "인생이힘드니", "조금지쳐", "폭발직전"]

####################################################################################
st.title("이전 결과 확인")

if len(history_df) == 0:
    st.image('./images/nulldata2.png')

else: 
    st.subheader("학업 스트레스 점수 추이")
    # 라인 차트 시각화
    with st.container(border=True):   
        # 데이터프레임을 Altair에 맞게 변환
        base_chart = alt.Chart(history_df_de).mark_line(point=True).encode(
            x=alt.X('date:T', title="날짜"),
            y=alt.Y('average_score:Q', scale=alt.Scale(domain=[0.5, 5.5]), title="학업 스트레스 점수"),
            color=alt.value("#000000")
        )

        # 구간별 척도 가로선 추가
        rule_data = pd.DataFrame({
            '학업 스트레스 단계': score_ranges,
            '구간': range_labels, 
            '색상': ['#277da1', '#90be6d', '#f9c74f', '#f8961e', '#f94144']  # 각 구간에 대해 다른 색상 지정

        })

        rule_chart = alt.Chart(rule_data).mark_rule(strokeDash=[5, 3]).encode(
            y='학업 스트레스 단계:Q',
            color=alt.Color('색상:N', scale=None)
        )

        final_chart = base_chart + rule_chart 

        st.altair_chart(final_chart, use_container_width=True)
        st.image('./images/스트레스 수치/스트레스5단계.png')

    # 리포트 탭
    st.subheader("날짜별 상세 결과 확인하기")

    for i in range(len(history_df_de)):
        # f-string 내부의 인용 부호 수정
        with st.expander(label=f"{history_df_de.loc[i, 'date']} : {history_df_de.loc[i, 'overall_summary']}"):
            st.metric(label="학업 스트레스 총점", value= f"{history_df_de.loc[i, 'average_score']:.2f}", )

            summary = history_df_de.loc[i, 'summary']
            summary_list = [sentence.strip() for sentence in summary.split('\n') if sentence]

            # 스트레스 원인
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


    for i in range(len(history_df_de)):    
        selected_date = st.selectbox(
            "측정 날짜", (history_df_de.loc[i, 'date'] + " : " + history_df_de.loc[i, 'overall_summary'])
        )

    # 같은 날 여러번 측정한 경우, 가장 최신 기록만 보여주도록 설정
    # part_idx = history_df_de.index[history_df_de["date"] == selected_date].tolist()[0]
    # st.subheader(f"{history_df_de.loc[part_idx, 'overall_summary']}" )

        # 비교
        with st.container(border=True):
            part_score = history_df_de.loc[i, 'average_score']
            part_percentile = history_df_de.loc[i, 'percentile']

            st.write(f"{user_name}님의 점수는 **{part_score:.1f}**/5.0으로, 100명 중 스트레스가 **{part_percentile:.1f}번째로** 많아요.")
                    
            def score_classification(score):
                for idx, upper_bound in enumerate(score_ranges):
                    if score <= upper_bound:
                        return idx
                    
            # 예시 데이터 생성
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
            score_min = part_score - 0.2
            score_max = part_score + 0.2
            x_fill = np.linspace(score_min, score_max, 100)
            y_fill = norm.pdf(x_fill, mu, std)


            stress_color = ['#277da1', '#90be6d', '#f9c74f', '#f8961e', '#f94144']  # 각 구간에 대해 다른 색상 지정

            part_color = stress_color[score_classification(part_score)]
            fig.add_trace(go.Scatter(x=x_fill, y=y_fill, fill='tozeroy', mode='none', name='당신의 스트레스 수치',
                                    fillcolor=part_color, opacity=0.3))

            fig.update_layout(title='학업 스트레스 점수의 PDF',
                            xaxis_title='학업 스트레스 점수',
                            yaxis_title='확률밀도함수',
                            legend_title='범례')
            st.plotly_chart(fig, use_container_width=True)

            score_img_list = ["고민이모니", "이정도는", "인생이", "조금지쳐", "폭발직전"]
            
            score_img_path = f"./images/스트레스 수치/스트레스_{score_img_list[score_classification(part_score)]}.png"
            st.image(score_img_path)

        with st.container():
            part_summary = history_df_de.loc[part_idx, 'summary']
            part_summary_list = [sentence.strip() for sentence in part_summary.split('\n') if sentence]
            part_stressor = part_summary_list[0].split(':')[0].strip()
            part_stressor_explain = part_summary_list[0].split(':')[1].strip() 
            part_stressor_icon = stressor_icons.get(part_stressor, '👌')

            part_symptom = part_summary_list[1].split(':')[0].strip()
            part_symptom_explain = part_summary_list[1].split(':')[1].strip() 
            part_symptom_icon = symptoms_icons.get(part_symptom, '👌')

            part_coping = part_summary_list[2].split(':')[0].strip()
            part_coping_explain = part_summary_list[2].split(':')[1].strip() 
            part_coping_icon = coping_icons.get(part_coping, '👌')

            with st.expander(f"학업 스트레스의 원인: {part_stressor_icon} {part_stressor}"):
                st.write(part_stressor_explain)
            
            with st.expander(f"학업 스트레스의 증상: {part_symptom_icon} {part_symptom}"):
                st.write(part_symptom_explain)
            
            with st.expander(f"학업 스트레스의 대처 전략: {part_coping_icon} {part_coping}"):
                st.write(part_coping_explain)

menu()