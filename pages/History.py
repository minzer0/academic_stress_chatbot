import streamlit as st
from result_dictionary import stressor_icons
from result_dictionary import symptoms_icons
from result_dictionary import coping_icons
from menu import menu
from dummy_data import df_sorted
from datetime import datetime
from st_supabase_connection import SupabaseConnection
import pandas as pd

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

history_df = df[(df['user_name'] == user_name) & 
                (df['user_id'] == user_id) &
                (df['date'] != str(current_date.year) + '-' + str(current_date.month) + '-' + str(current_date.day))]

history_df_as = history_df.sort_values(by='date', ascending=True)
history_df_as.rename(columns={"date": "날짜", "average_score": "스트레스 점수"}, inplace=True)
history_df_as.reset_index(drop=True, inplace=True)

history_df_de = history_df.sort_values(by='date', ascending=False)
history_df_de.reset_index(drop=True, inplace=True)

########################################################################################

st.title("이전 결과 확인")

if len(history_df) == 0:
    st.image('./images/nulldata2.png')

else: 
    # 탭을 사용할 경우 (간단한 탭 구현)
    tabs = st.tabs(["점수 추이", "대화별 상세 내역"])

    # 홈 탭
    with tabs[0]:
        st.subheader("학업 스트레스 점수 추이")
        # 라인 차트 시각화
        st.line_chart(history_df_as, x="날짜", y="스트레스 점수")

    # 리포트 탭
    with tabs[1]:
        st.subheader("대화별 상세 내역 보기")

        for i in range(len(history_df_de)):
            # f-string 내부의 인용 부호 수정
            with st.expander(label=f"{history_df_de.loc[i, 'date']} : {history_df_de.loc[i, 'overall_summary']}"):
                st.metric(label="학업 스트레스 총점", value= f"{df_sorted.loc[i, 'average_score']:.2f}", )

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

                # st.write("스트레스 원인:")
                # st.write(f"- {df_sorted.loc[i, '스트레스 원인']} {stressor_icons.get(df_sorted.loc[i, '스트레스 원인'], '👌')}")
                # st.write("스트레스 증상:")
                # st.write(f"- {df_sorted.loc[i, '스트레스 증상']} {symptoms_icons.get(df_sorted.loc[i, '스트레스 증상'], '👌')}")
                # st.write("스트레스 대처 전략:")
                # st.write(f"- {df_sorted.loc[i, '스트레스 대처 전략']} {coping_icons.get(df_sorted.loc[i, '스트레스 대처 전략'], '👌')}")

col1, col2, col3 = st.columns(3)
with col2:
    main_button = st.button(label = "🏠   홈 화면으로 돌아가기", key=1)
    if main_button:
        st.switch_page("pages/Home.py")

menu()