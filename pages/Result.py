import streamlit as st
from st_supabase_connection import SupabaseConnection

from result_dictionary import stressor_icons
from result_dictionary import symptoms_icons
from result_dictionary import coping_icons
from menu import menu

# from backend import average_score, percentile, summary, overall_summary
from backend import backend
from dummy_data import df_sorted

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


st_supabase_client = st.connection("supabase",type=SupabaseConnection)

if "user_id" not in st.session_state:
    st.error("로그인이 필요합니다.")
    if st.button("로그인하러 가기"):
        st.switch_page("pages/Login.py")
    st.stop()

user_id = st.session_state["user_id"]
user_name = st.session_state["user_metadata"]["user_name"]

exec(open('backend.py').read())

summary_list = [sentence.strip() for sentence in summary.split('.') if sentence]
########################################################################################

# 메인 헤더
st.header("학업 스트레스 검사 결과")

if average_score is None:
    st.image('./images/nulldata.png')
else:
    # 사용자 학업 스트레스 점수와 해당 구간의 사람 수 표시
    st.write(f"{user_name}님의 점수는 **{average_score}**점이에요.")

    # 아이콘 및 정보 섹션# 열을 사용하여 레이아웃 구성
    col1, col2, col3 = st.columns(3)

    with col1:
        # 스트레스 점수 정보
        st.markdown("### 스트레스 수치")
        st.write(f":red[상위 {average_score}%]")  # 스트레스 점수를 빨간색으로 표시

    with col2:
        # 스트레스 원인 정보
        st.markdown("### 스트레스 원인")
        stressor = summary_list[0]
        stressor_icon = stressor_icons.get(stressor.split(':')[0].strip(), '👌')
        st.write(f"{stressor} {stressor_icon}")

    with col3:
        # 스트레스 대처 전략 정보
        st.markdown("### 스트레스 대처 전략")
        coping = summary_list[2]
        coping_icon = coping_icons.get(coping.split(':')[0].strip(), '👌')
        st.write(f"{coping} {coping_icon}")

    # 추가 정보 (스트레스 증상)
    st.markdown("### 스트레스 증상")
    for i in range(3):  # 증상 정보를 반복 출력
        symptom = summary_list[1]
        symptom_icon = symptoms_icons.get(symptom.split(':')[0].strip(), '👌')
        st.write(f"- {symptom} {symptom_icon}")

    st.write("#")

    st.subheader("학업 스트레스 점수 추이")

    # 라인 차트 시각화
    st.line_chart(df_sorted, x="날짜", y="스트레스 점수")

col1, col2, col3 = st.columns(3)
with col2:
    if st.button(":bar_chart:    이전 기록 확인하기",
            use_container_width=True):
        st.switch_page("pages/History.py")
    if st.button("🏠   메인 화면으로 돌아가기",
            use_container_width=True, ):
        st.switch_page("pages/Chatbot.py")

menu()