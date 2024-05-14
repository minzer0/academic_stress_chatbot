import streamlit as st
import numpy as np
import altair as alt
import pandas as pd
from function.menu import menu
from datetime import datetime
from st_supabase_connection import SupabaseConnection
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import norm
# from wordcloud import WordCloud

# from function.dummy_data import df_sorted
from function.result_dictionary import stressor_icons
from function.result_dictionary import symptoms_icons
from function.result_dictionary import coping_icons

# from Result import stressor, stressor_icon, symptom, symptom_icon, coping, coping_icon

########################################################################################
### UI SETUP 

st.set_page_config(
    page_title = "고민모니",
    page_icon = "./images/logo.png"
)

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
header_1, header_2 = st.columns(2)
with header_1:
    st.title("고민모니")

    # st.text(f"{user_name}님",) # 오른쪽 정렬 필요
    # 로그아웃 및 정보 수정 페이지 필요
    # st.button()

listTabs = [
    "대시보드",
    "상세보기",
    "전체변화",
    "고민모니?",

]
tabs = st.tabs(listTabs)


with tabs[0]:
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
        
        cols = st.columns(3)

        # 스트레스 원인
        with cols[0]:
            with st.expander(f"원인: {stressor_icon} {stressor}"):
                st.write(stressor_explain)

        # 스트레스 증상
        with cols[1]:
            with st.expander(f"증상: {symptom_icon} {symptom}"):
                st.write(symptom_explain)

        # 스트레스 대처 전략
        with cols[2]:
            with st.expander(f"대처 전략: {coping_icon} {coping}"):
                st.write(coping_explain)

with tabs[1]:
    selected_date = st.selectbox(
        "측정 날짜", history_df_de['date']
    )

    # 같은 날 여러번 측정한 경우, 가장 최신 기록만 보여주도록 설정
    part_idx = history_df_de.index[history_df_de["date"] == selected_date].tolist()[0]
    st.subheader(f"{history_df_de.loc[part_idx, 'overall_summary']}" )

    # 비교
    with st.container(border=True):
        part_score = history_df_de.loc[part_idx, 'average_score']
        part_percentile = history_df_de.loc[part_idx, 'percentile']

        st.write(f"{user_name}님의 점수는 **{part_score:.1f}**/5.0으로, 100명 중 스트레스가 **{part_percentile:.1f}번째로** 많아요.")
                
        def score_classification(score):
            for idx, upper_bound in enumerate(score_ranges):
                if score <= upper_bound:
                    return idx
                
        # 예시 데이터 생성
        np.random.seed(0)
        dummy_scores = np.random.normal(3.773399014778325, 0.9273521676028207, 1000)
        mu, std = np.mean(dummy_scores), np.std(dummy_scores)  # 평균과 표준편차 계산

        # PDF 그래프 생성
        def plot_pdf(data, user_score):
            sns.set(style="whitegrid")
            plt.figure(figsize=(8, 4))
            x = np.linspace(min(data), max(data), 1000)
            y = norm.pdf(x, mu, std)  # 확률밀도함수
            plt.plot(x, y, 'k', lw=2)
            # 사용자 점수 위치 표시
            plt.axvline(x=user_score, color='r', linestyle='--')
            plt.xlabel('학업 스트레스 점수')
            plt.ylabel('Probability Density')
            plt.title('학업 스트레스 점수의 PDF')
            plt.legend(['확률밀도함수', '사용자 점수'])
            st.pyplot(plt)

        # 스트림릿에서 그래프 출력
        plot_pdf(dummy_scores, part_score)

        # # 사용자 학업 스트레스 점수와 해당 구간의 사람 수 표시
        # st.write("**:blue[파란색]**: 나와 비슷한 점수(+/-5)를 가진 사람들 ")

        # # 데이터 생성
        # np.random.seed(0) # 재현성을 위해 랜덤 시드 설정
        # n_samples = 100  # 샘플 수

        # # 정규분포 데이터 생성
        # dist_data = np.random.normal(3.773399014778325, 0.9273521676028207, n_samples)
        # dist_df = pd.DataFrame(dist_data, columns=['score'])

        # # 히스토그램 생성
        # base_histogram = (
        #     alt.Chart(dist_df)
        #     .mark_bar()
        #     .encode(
        #         x=alt.X("score:Q", bin=alt.Bin(extent=[1.0, 5.0], step=0.5)),  # 5점 간격으로 분할
        #         y="count()",
        #         color=alt.value("lightgray")
        #     )
        # )

        # # 특정 영역 강조
        # highlight = (
        #     alt.Chart(dist_df[dist_df['score'].between(average_score-0.1, average_score+0.1)])  # 점수 기준 +/-5 범위
        #     .mark_bar(color='#FFB6C1')  # 강조 색상 설정
        #     .encode(
        #         x=alt.X("score:Q", bin=alt.Bin(extent=[1.0, 5.0], step=0.5)),
        #         y="count()",
        #     )
        # )

        # # 히스토그램과 강조 영역 결합
        # final_chart = base_histogram + highlight

        # # 차트 렌더링
        # st.altair_chart(final_chart, use_container_width=True)
        

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

with tabs[2]:
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
        
    with st.container(border=True):
        cols = st.columns(3)
        with cols[0]:
            st.write("학업 스트레스 원인 키워드")
        with cols[1]:
            st.write("학업 스트레스 증상 키워드")
        with cols[2]:
            st.write("학업 스트레스 대처전략 키워드")

        # # Create some sample text
        # text = 'Fun, fun, awesome, awesome, tubular, astounding, superb, great, amazing, amazing, amazing, amazing'

        # # Create and generate a word cloud image:
        # wordcloud = WordCloud().generate(text)

        # # Display the generated image:
        # plt.imshow(wordcloud, interpolation='bilinear')
        # plt.axis("off")
        # plt.show()
        # st.pyplot(plt)


with tabs[3]:
    st.write("고민모니는 학생들의 학업 스트레스를 개선하기 위해 고안되었어요.")
    st.image('./images/HAI_logo.png')

st.write("#")
if st.button(":left_speech_bubble:   모니와 대화하며 \n :red[**새로운 학업 스트레스 측정**하기]",
            use_container_width=True, ):
    st.switch_page("pages/Chatbot.py")

menu()
