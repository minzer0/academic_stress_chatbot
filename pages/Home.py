import streamlit as st
from dummy_data import df_sorted
from result_dictionary import stressor_icons
from result_dictionary import symptoms_icons
from result_dictionary import coping_icons

if "user_metadata" not in st.session_state:
    st.error("로그인이 필요합니다.")
    if st.button("로그인하러 가기"):
        st.switch_page("pages/Login.py")
    st.stop()

st.title(f"{st.session_state['user_metadata']['user_name'][1:]}님의 학업 스트레스 지수")

with st.container(border=True):
    st.markdown("또래 100명 중..")

col1, col2, col3 = st.columns(3)

# 스트레스 원인
with col1:
    st.subheader("스트레스 원인")
    st.write(f"- {df_sorted.loc[-1, '스트레스 원인']} {stressor_icons.get(df_sorted.loc[-1, '스트레스 원인'], '👌')}")

# 스트레스 증상
with col2:
    st.subheader("스트레스 증상")
    st.write(f"- {df_sorted.loc[-1, '스트레스 증상']} {symptoms_icons.get(df_sorted.loc[-1, '스트레스 증상'], '👌')}")

# 스트레스 대처 전략
with col3:
    st.subheader("스트레스 대처 전략")
    st.write(f"- {df_sorted.loc[-1, '스트레스 대처 전략']} {coping_icons.get(df_sorted.loc[-1, '스트레스 대처 전략'], '👌')}")



if st.button(":left_speech_bubble:   모니와 대화하며 **새로운 학업 스트레스 측정**하기",
            use_container_width=True, ):
    st.switch_page("pages/Chatbot.py")
if st.button(":bar_chart:    이전 기록 확인하기",
             use_container_width=True):
    st.switch_page("pages/History.py")