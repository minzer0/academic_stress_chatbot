import streamlit as st
import numpy as np
import pandas as pd
import plotly as plt

from result_dictionary import stressor_icons
from result_dictionary import symptoms_icons
from result_dictionary import coping_icons

st.set_page_config(
    page_title = "고민모니",
    page_icon = "./images/Okay_icon.png"
)

####### Main Home ###########
# 1. Title: 고민모니
# 2. SubHeader: ㅇㅇ 님의 학업 스트레스 지수
# 3. [지난 기록 다시보기] icon dashboard 형식으로 보여주기
# 4. [학업스트레스 측정] button -> chat.py로 연결
# 5. [이전 결과 확인] button -> total_result.py로 연결
#############################

# 사전 데이터
user_info = {
    'name' : '다나',
    'age' : 23,
    'last_test_day' : '03/31',
    "last_score" : 78,
}

user_data = {'last_stressor' : ["동료와의 경쟁", "평가와 시험", ""],
    'last_symptom' : ["소화 문제", "불안", "음식 섭취 증가 또는 감소"],
    "last_coping" : ["당당한 태도", "", ""]}

############################
st.markdown("<h1 style='font-family:Nanum Gothic;'>고민모니💭</h1>", unsafe_allow_html=True)
st.caption("👯 Academic Stress Assessment Chatbot produced by 유박사 👯")

st.image('./images/introduction.png', caption='고민모니는 여러분의 회복 탄력성 향상을 도와드릴 수 있어요!')


user_name = user_info["name"]
last_score = user_info['last_score']

last_test_day = user_info['last_test_day']
st.text(f"마지막으로 측정한 {user_name} 님의 학업 스트레스 결과는...")
# st.text(f"{user_name} 님의 학업 스트레스 결과는...")
    
col1, col2, col3 = st.columns(3)

# 스트레스 원인
with col1:
    st.subheader("스트레스 원인")
    st.write("\n".join(f"- {cause} {stressor_icons.get(cause, '👌')}" for cause in user_data["last_stressor"]))

# 스트레스 증상
with col2:
    st.subheader("스트레스 증상")
    st.write("\n".join(f"- {symptom} {symptoms_icons.get(symptom, '👌')}" for symptom in user_data["last_symptom"]))

# 스트레스 대처 전략
with col3:
    st.subheader("스트레스 대처 전략")
    st.write("\n".join(f"- {strategy} {coping_icons.get(strategy, '👌')}" for strategy in user_data["last_coping"]))


chat_button = st.button(label = ":left_speech_bubble:   모니와 대화하며 **새로운 학업 스트레스 측정**하기",
                        use_container_width=True, )
total_result_button = st.button(label = ":bar_chart:    이전 결과 확인하기",
                                use_container_width=True)

if chat_button:
    st.switch_page("pages/chat.py")
elif total_result_button:
    st.switch_page("pages/total_result.py")