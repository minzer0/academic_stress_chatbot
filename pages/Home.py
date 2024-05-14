import streamlit as st
import numpy as np
import altair as alt
import pandas as pd
from datetime import datetime
from st_supabase_connection import SupabaseConnection

import matplotlib.pyplot as plt
from wordcloud import WordCloud
from streamlit_navigation_bar import st_navbar
import pages as pg
import matplotlib.font_manager as fm

from function.result_dictionary import stressor_icons
from function.result_dictionary import symptoms_icons
from function.result_dictionary import coping_icons

########################################################################################
### UI SETUP 

st.set_page_config(
    page_title = "고민모니",
    page_icon = "./images/logo.png",
    initial_sidebar_state="collapsed"
)

# .streamlit/style.css 파일 열기
with open("./.streamlit/style.css") as css:
    # CSS 파일을 읽어와서 스타일 적용
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)

page = st_navbar(["대시보드", "상세보기", "고민모니?", "내프로필"])


sys_font = fm.findSystemFonts()
nanum_fonts = [f for f in sys_font if 'Nanum' in f]
# path ='C:/Users/Dana You/Downloads/nanum-all/나눔 글꼴/나눔스퀘어/NanumFontSetup_OTF_SQUARE/NanumSquareR.otf'

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

data_empty = False
if len(history_df) == 0:
    data_empty = True



# 정석대로 하면.. score_ranges = [1.94, 3.09, 3.72, 4.39, 4.92, 5.0]
score_ranges = [1.94, 3.09, 3.72, 4.39, 5.0]
range_labels = ["고민이모니", "이정도는OK", "인생이힘드니", "조금지쳐", "폭발직전"]


########################################################################################
if page == "대시보드":
    st.header("학업 스트레스 측정 요약")
    with st.container(border=True):
        st.subheader("학업 스트레스 수치")
        
        # 데이터프레임을 Altair에 맞게 변환
        base_chart = alt.Chart(history_df_de).mark_line(point=True).encode(
            x='date:T',
            y=alt.Y('average_score:Q', scale=alt.Scale(domain=[0.5, 5.5]), title="학업 스트레스 수치"),
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
        st.subheader("가장 최근에 측정한 학업 스트레스의...")
        
        stressor_list = '손톱뜯기, 손톱뜯기, 피로'

        # def wordcolud_show(text):
        #     wordcloud = WordCloud(width=200, height=200,
        #                         background_color='white',
        #                         max_words=20,
        #                         contour_width=3,
        #                         contour_color='Set2',
        #                         font_path=path).generate(text)     
        #     # Display the generated image:
        #     plt.imshow(wordcloud, interpolation='bilinear')
        #     plt.axis("off")
        #     plt.show()
        #     st.pyplot(plt)

        # 스트레스 원인
        cols = st.columns(3)
        with cols[0]:
            st.write("학업 스트레스 원인 키워드")
            # wordcolud_show(stressor_list)
        with cols[1]:
            st.write("학업 스트레스 증상 키워드")
            # wordcolud_show(stressor_list)
        with cols[2]:
            st.write("학업 스트레스 대처전략 키워드")
            # wordcolud_show(stressor_list)

if page == "상세보기":
    st.switch_page("pages/Home.py")

if page == "고민모니?":
    st.switch_page("pages/About.py")

if page == "내프로필":
    st.write("프로필")


st.write("#")
if st.button(":left_speech_bubble:   모니와 대화하며 \n :red[**새로운 학업 스트레스 측정**하기]",
            use_container_width=True, ):
    st.switch_page("pages/Chatbot.py")
