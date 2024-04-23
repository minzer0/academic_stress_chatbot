import streamlit as st
from result_dictionary import stressor_icons
from result_dictionary import symptoms_icons
from result_dictionary import coping_icons

from dummy_data import df_sorted

st.title("결과")

st.subheader("학업 스트레스 점수 추이", divider='grey')


# 라인 차트 시각화
st.line_chart(df_sorted, x="날짜", y="스트레스 점수")

main_button = st.button(label = "🏠   메인 화면으로 돌아가기")

if main_button:
    st.switch_page("pages/Home.py")

st.subheader("대화별 상세 내역 보기", divider='grey')

for i in range(len(df_sorted)):
    # f-string 내부의 인용 부호 수정
    with st.expander(label=f"{df_sorted.loc[i, '날짜']} : {df_sorted.loc[i, '대화 주요 내용']}"):
        st.metric(label="학업 스트레스 총점", value=df_sorted.loc[i, '스트레스 점수'], )

        st.write("스트레스 원인:")
        st.write(f"- {df_sorted.loc[i, '스트레스 원인']} {stressor_icons.get(df_sorted.loc[i, '스트레스 원인'], '👌')}")
        st.write("스트레스 증상:")
        st.write(f"- {df_sorted.loc[i, '스트레스 증상']} {symptoms_icons.get(df_sorted.loc[i, '스트레스 증상'], '👌')}")
        st.write("스트레스 대처 전략:")
        st.write(f"- {df_sorted.loc[i, '스트레스 대처 전략']} {coping_icons.get(df_sorted.loc[i, '스트레스 대처 전략'], '👌')}")

        if st.button("자세한 대화 내용 확인하기", key=i):
            st.switch_page("pages/History.py")
