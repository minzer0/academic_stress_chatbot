from openai import OpenAI
import streamlit as st
import pandas as pd
import os

from datetime import datetime
from st_supabase_connection import SupabaseConnection


st_supabase_client = st.connection("supabase",type=SupabaseConnection)
try:
    st_supabase_client.table("chat").select("user_name, message").execute()
except Exception as e:
    st.write(e)

if "user_id" not in st.session_state:
    st.error("로그인이 필요합니다.")
    if st.button("로그인하러 가기"):
        st.switch_page("pages/Login.py")
    st.stop()
    
user_id = st.session_state["user_id"]
user_name = st.session_state["user_metadata"]["user_name"]

st.markdown("<h1 style='font-family:Nanum Gothic;'>모니와 대화하기💭</h1>", unsafe_allow_html=True)
st.caption("👯 Academic Stress Assessment Chatbot produced by 유박사 👯")


# Set a default model
if "openai_model" not in st.session_state:    
    st.session_state["openai_model"] = "gpt-4-0125-preview"


# Set OpenAI API key 
client = OpenAI(api_key=st.secrets['OPENAI_API_KEY'], 
                organization=st.secrets['OPENAI_ORGANIZATION'])
openai_api_key = st.secrets['OPENAI_API_KEY']


# Initialize chat history
if "conversation_history" not in st.session_state:    
    st.session_state.conversation_history = [
        {"role": "system", "content": st.secrets['system_prompt']},
        {"role": "assistant", "content": f"안녕 {user_name[1:]}! 나는 모니라고 해😊"}
    ]


# Display chat messages from history on app rerun
for message in st.session_state.conversation_history:        
    if message["role"]=='system':
        continue
    st.chat_message(message["role"]).write(message["content"]) 
    print(message) 

 
if user_input := st.chat_input():
            
    #Add user message to chat history
    st.session_state.conversation_history.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)
        

    with st.spinner('모니가 입력 중입니다...'):
        #response generation
        response = client.chat.completions.create(
            model=st.session_state["openai_model"], 
            messages=st.session_state.conversation_history,
            #stream=True,
            max_tokens=1000,
            temperature=0.7,      
            )

        assistant_reply = response.choices[0].message.content
        st.session_state.conversation_history.append({"role": "assistant", "content": assistant_reply})
        st.chat_message("assistant").write(assistant_reply)
        
        # Store user and assistant message to database
        st_supabase_client.table("chat").insert(
            [
                {
                    "user_id": user_id,
                    "user_name": user_name,
                    "role": "user",
                    "message": user_input,
                    "created_at": datetime.now().isoformat()
                },
                {
                    "user_id": user_id,
                    "user_name": user_name,
                    "role": "assistant",
                    "message": assistant_reply,
                    "created_at": datetime.now().isoformat()
                }
            ]
        ).execute()
        
        if "<대화가 종료되었습니다.>" in assistant_reply:
            st.switch_page("pages/Result.py")


with st.sidebar:
    st.sidebar.header('이전 대화 기록 확인하기')
    # st.sidebar.button("로그 저장", on_click=save_conversation_to_file(st.session_state["conversation_history"]))

