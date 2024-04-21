# from openai import OpenAI
# import streamlit as st
# import pandas as pd
# import os


# st.markdown("<h1 style='font-family:Nanum Gothic;'>모니와 대화하기💭</h1>", unsafe_allow_html=True)
# st.caption("👯 Academic Stress Assessment Chatbot produced by 유박사 👯")


# # Set a default model
# if "openai_model" not in st.session_state:    
#     st.session_state["openai_model"] = "gpt-4-0125-preview"


# # Set OpenAI API key 
# client = OpenAI(api_key=st.secrets['OPENAI_API_KEY'], 
#                 organization=st.secrets['OPENAI_ORGANIZATION'])
# openai_api_key = st.secrets['OPENAI_API_KEY']


# # Initialize chat history
# if "conversation_history" not in st.session_state:    
#     st.session_state.conversation_history = [
#         {"role": "system", "content": st.secrets['system_prompt']},
#         {"role": "assistant", "content": "안녕! 나는 모니라고 해😊"}
#     ]


# # Display chat messages from history on app rerun
# for message in st.session_state.conversation_history:        
#     if message["role"]=='system':
#         continue
#     st.chat_message(message["role"]).write(message["content"]) 
#     print(message) 

 
# if user_input := st.chat_input():    
#     #Add user message to chat history
#     st.session_state.conversation_history.append({"role": "user", "content": user_input})
#     st.chat_message("user").write(user_input)
        

#     with st.spinner('모니가 입력 중입니다...'):
#         #챗봇 응답 생성
#         response = client.chat.completions.create(
#             model=st.session_state["openai_model"], 
#             messages=st.session_state.conversation_history,
#             #stream=True,
#             max_tokens=1000,
#             temperature=0.7,      
#             )

#         assistant_reply = response.choices[0].message.content
#         st.session_state.conversation_history.append({"role": "assistant", "content": assistant_reply})
#         st.chat_message("assistant").write(assistant_reply)  

#         #사용자별 대화 세션 저장
#         if not os.path.exists('user_conv_log.csv'):
#             with open('user_conv_log.csv', mode='w', newline='', encoding='cp949') as file:
#                 writer = csv.writer(file)
#                 writer.writerow(['user_ip', 'timestamp', 'user_message', 'assistant_message'])
    
#         user_ip = request.client.host
#         timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
#         user_conv_log = [user_ip, timestamp, user_message, assistant_message]
    
#         # Write user_conv_log to CSV file
#         with open('user_conv_log.csv', mode='a', newline='', encoding='cp949') as file:
#             writer = csv.writer(file)
#             writer.writerow(user_conv_log)


# # Previous conversation
# CSV_FILE = "user_conv_log.csv"
# try:
#     chat_history_df = pd.read_csv(CSV_FILE)
# except FileNotFoundError:
#     chat_history_df = pd.DataFrame(columns=['user_ip', 'timestamp', 'user_message', 'assistant_message'])


# # def get_button_label(user_conv_log, user_ip):
# #     first_message = user_conv_log[(user_conv_log["user_ip"] == user_ip) & (user_conv_log["Role"] == "User")].iloc[0]["Content"]
# #     return f"Chat {chat_id[0:7]}: {' '.join(first_message.split()[:5])}..."


# # for chat_id in chat_history_df["user_ip"].unique():
# #     button_label = get_button_label(chat_history_df, chat_id)
# #     if st.sidebar.button(button_label):
# #         current_chat_id = chat_id
# #         loaded_chat = chat_history_df[chat_history_df["ChatID"] == chat_id]
# #         loaded_chat_string = "\n".join(f"{row['Role']}: {row['Content']}" for _, row in loaded_chat.iterrows())
# #         st.text_area("채팅 기록", value=loaded_chat_string, height=300)

# with st.sidebar:
#     st.sidebar.header('이전 대화 기록 확인하기')
#     # st.sidebar.button("로그 저장", on_click=save_conversation_to_file(st.session_state["conversation_history"]))




from openai import OpenAI
import streamlit as st
import pandas as pd
import os
import csv  # csv 모듈을 import합니다
import datetime  # datetime 모듈을 import합니다
from streamlit.report_thread import get_report_ctx  # get_report_ctx 함수를 import합니다


st.markdown("<h1 style='font-family:Nanum Gothic;'>모니와 대화하기💭</h1>", unsafe_allow_html=True)
st.caption("👯 Academic Stress Assessment Chatbot produced by 유박사 👯")

# Set a default model
if "openai_model" not in st.session_state:    
    st.session_state["openai_model"] = "gpt-4-0125-preview"

client = OpenAI(api_key=st.secrets['OPENAI_API_KEY'], 
                organization=st.secrets['OPENAI_ORGANIZATION'])
openai_api_key = st.secrets['OPENAI_API_KEY']

if "conversation_history" not in st.session_state:    
    st.session_state.conversation_history = [
        {"role": "system", "content": st.secrets['system_prompt']},
        {"role": "assistant", "content": "안녕! 나는 모니라고 해😊"}
    ]

for message in st.session_state.conversation_history:        
    if message["role"] == 'system':
        continue
    st.chat_message(message["role"]).write(message["content"]) 

if user_input := st.chat_input():    
    st.session_state.conversation_history.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    with st.spinner('모니가 입력 중입니다...'):
        response = client.chat.completions.create(
            model=st.session_state["openai_model"], 
            messages=st.session_state.conversation_history,
            max_tokens=1000,
            temperature=0.7,
        )

        assistant_reply = response.choices[0].message.content
        st.session_state.conversation_history.append({"role": "assistant", "content": assistant_reply})
        st.chat_message("assistant").write(assistant_reply)  

        # 사용자의 입력과 챗봇 응답을 변수에 할당합니다.
        user_message = user_input
        assistant_message = assistant_reply

        # 사용자별 대화 세션 저장
        if not os.path.exists('user_conv_log.csv'):
            with open('user_conv_log.csv', mode='w', newline='', encoding='cp949') as file:
                writer = csv.writer(file)
                writer.writerow(['user_ip', 'timestamp', 'user_message', 'assistant_message'])

        # request와 datetime 모듈을 사용하여 사용자의 IP 주소와 현재 시간을 가져옵니다.
        ctx = get_report_ctx()
        user_ip = ctx.request.client.host
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 사용자별 대화 세션을 리스트로 만듭니다.
        user_conv_log = [user_ip, timestamp, user_message, assistant_message]

        # Write user_conv_log to CSV file
        with open('user_conv_log.csv', mode='a', newline='', encoding='cp949') as file:
            writer = csv.writer(file)
            writer.writerow(user_conv_log)

# Previous conversation
CSV_FILE = "user_conv_log.csv"
try:
    chat_history_df = pd.read_csv(CSV_FILE)
except FileNotFoundError:
    chat_history_df = pd.DataFrame(columns=['user_ip', 'timestamp', 'user_message', 'assistant_message'])

with st.sidebar:
    st.sidebar.header('이전 대화 기록 확인하기')

