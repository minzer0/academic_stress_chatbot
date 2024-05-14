import streamlit as st
from streamlit_navigation_bar import st_navbar
from function.menu import menu

# .streamlit/style.css 파일 열기
with open("./.streamlit/style.css") as css:
    # CSS 파일을 읽어와서 스타일 적용
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)

####################################################################################
st.title("고민모니에 대해 알려드릴게요!")

st.subheader("고민모니가 왜 필요할까?")

why_go = "학생의 학업 스트레스는 정신건강에 치명적인 영향을 미치는 중대한 사회 문제로 대두되고 있다. \
    교육부가 2022년 발표한 ‘학생 정신건강 실태 조사’에 따르면, 코로나 이후 학생 43.2%가 학업 스트레스를 겪고 있다고 말한 것으로 밝혀졌다.\
    학업 스트레스는 우울증 및 자살 충동으로 이어질 수 있으며 지속될 경우, 정신 병리의 위험성을 20배까지 높일 수 있다. "

st.write(why_go)

st.subheader("고민모니는 어떻게 학업 스트레스를 평가할까?")
how_go = "고민모니는 기존 학업 스트레스 측정을 위한 자가 설문 중 하나인 SISCO-AS를 기반으로 설계되었으며, \
    대상자에게 학업 스트레스의 원인, 그에 따른 물리적, 심리적, 행동적 증상, 그리고 대처 방안에 대해 순차적으로 묻는다. \
    챗봇은 질문하기 전 질문과 관련된 자신의 고민을 먼저 털어놓음으로써 대상자의 자기 성찰을 유도한다. "

st.write(how_go)
st.image('./images/go_structure.png')

st.subheader("고민모니가 다른 것보다 좋은 이유는 뭘까?")
good_go = "고민모니는 학업 스트레스 측정 과정에서 자가 설문 문항을 그대로 물어보는 규칙 모델 기반 설계에서 벗어나 \
    대규모 언어 모델의 프롬프트 엔지니어링을 통해 자기 노출을 제공하는 챗봇과 자연스러운 대화가 가능하다는 것이다. \
    또한, 사용자와 챗봇과의 대화 로그 데이터를 학업 스트레스 점수로 전환하는 새로운 접근법을 통해 챗봇과의 대화만으로도 \
    학업 스트레스의 정확한 측정을 위한 기반을 마련한다. "

st.write(good_go)
st.image('./images/go_comparision.png')

menu()