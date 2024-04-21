import streamlit as st
from main import user_info
from main import user_data

from result_dictionary import stressor_icons
from result_dictionary import symptoms_icons
from result_dictionary import coping_icons

from dummy_data import df_sorted

st.set_page_config(
    page_title = "고민모니",
    page_icon = "./images/Okay_icon.png"
)

st.title("고민모니")
st.subheader("전체 검사 결과", divider='grey')

# 라인 차트 시각화
st.line_chart(df_sorted, x="날짜", y="스트레스 점수")

main_button = st.button(label = "🏠   메인 화면으로 돌아가기",
                        use_container_width=True, )
if main_button:
    st.switch_page("main.py")

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
        