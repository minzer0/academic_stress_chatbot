import streamlit as st
import altair as alt
import pandas as pd
from datetime import datetime
from st_supabase_connection import SupabaseConnection

from function.menu import menu

from function.result_dictionary import stressor_icons
from function.result_dictionary import symptoms_icons
from function.result_dictionary import coping_icons

########################################################################################
### UI SETUP 

st.set_page_config(
    page_title = "고민모니",
    page_icon = "./images/logo.png",
    initial_sidebar_state="collapsed",
)

#######################################################################################
# .streamlit/style.css 파일 열기
with open("./.streamlit/style.css") as css:
    # CSS 파일을 읽어와서 스타일 적용
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)


### DATA SETUP

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

# 오늘 날짜의 새로운 df
filtered_df = df[(df['user_name'] == user_name) & 
                 (df['user_id'] == user_id) &
                 (df['date'] == str(current_date.year) + '-' + str(current_date.month) + '-' + str(current_date.day))]
filtered_df.reset_index(drop=True, inplace=True)
# 과거 df
history_df = df[(df['user_name'] == user_name) & 
                (df['user_id'] == user_id) &
                (df['date'] != str(current_date.year) + '-' + str(current_date.month) + '-' + str(current_date.day))]
# 날짜별로 sort된 과거 df
history_df_de = history_df.sort_values(by='date', ascending=False)
history_df_de.reset_index(drop=True, inplace=True)

if len(history_df) == 0:
    st.image('./images/nulldata.png')

else:

    # summary: 가장 최신 날짜 summary (string), summary_list: 가장 최신 날짜 증상/원인/대처전략 (list)
    summary = history_df_de.loc[0, 'summary']
    summary_list = [sentence.strip() for sentence in summary.split('\n') if sentence]

    ### USER DATA
    average_score = history_df_de.loc[0, 'average_score']
    percentile = history_df_de.loc[0, 'percentile']

    # 가장 최신 날짜 summary define
    stressor = summary_list[0].split(':')[0].strip()
    stressor_explain = summary_list[0].split(':')[1].strip() 
    stressor_icon = stressor_icons.get(stressor, '👌')

    symptom = summary_list[1].split(':')[0].strip()
    symptom_explain = summary_list[1].split(':')[1].strip() 
    symptom_icon = symptoms_icons.get(symptom, '👌')

    coping = summary_list[2].split(':')[0].strip()
    coping_explain = summary_list[2].split(':')[1].strip() 
    coping_icon = coping_icons.get(coping, '👌')


    # 정석대로 하면.. score_ranges = [1.94, 3.09, 3.72, 4.39, 4.92, 5.0]
    score_ranges = [1.94, 3.09, 3.72, 4.39, 5.0]
    range_labels = ["고민이모니", "이정도는OK", "인생이힘드니", "조금지쳐", "폭발직전"]


    ########################################################################################

    st.markdown("# 학업 스트레스 측정 요약")
    with st.container(border=True):
        st.subheader("학업 스트레스 점수 추이")
        
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


    with st.container():
        st.subheader(f"가장 최근에 측정한 ({history_df_de.loc[0, 'date']}) 학업 스트레스")

        # 스트레스 원인
        cols = st.columns(3)
        with st.expander(f"학업 스트레스의 원인: {stressor_icon} {stressor}"):
            st.write(stressor_explain)
        
        with st.expander(f"학업 스트레스의 증상: {symptom_icon} {symptom}"):
            st.write(symptom_explain)
        
        with st.expander(f"학업 스트레스의 대처 전략: {coping_icon} {coping}"):
            st.write(coping_explain)

st.write("#")
if st.button(":left_speech_bubble:   모니와 대화하며 \n :red[**새로운 학업 스트레스 측정**하기]",
            use_container_width=True, ):
    st.switch_page("pages/Chatbot.py")

menu()