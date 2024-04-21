from openai import OpenAI
import streamlit as st


st.title("Career Counseling Chatbot💬")
st.caption("🚀 AI Career Counselor Conversational Assistant produced by Hyerim")


# Set a default model
if "openai_model" not in st.session_state:    
    st.session_state["openai_model"] = "gpt-4-1106-preview"

# Set OpenAI API key 
client = OpenAI(api_key=st.secrets['OPENAI_API_KEY'], 
                organization=st.secrets['OPENAI_ORGANIZATION'])
openai_api_key = st.secrets['OPENAI_API_KEY']


# Initialize chat history
if "conversation_history" not in st.session_state:    
    st.session_state.conversation_history = [
        {"role": "system", "content": st.secrets['system_prompt']},
        {"role": "assistant", "content": "안녕하세요! 저는 당신의 AI 진로 상담사입니다. 당신의 이름은 무엇인가요?"}
    ]


# Display chat messages from history on app rerun
for message in st.session_state.conversation_history:        
    if message["role"]=='system':
        continue
    st.chat_message(message["role"]).write(message["content"]) 
    print(message) 


 
 
if user_input := st.chat_input():    
    #Add user message to chat history
    #st.session_state.messages.append({"role": "system", "content": system_prompt})
    st.session_state.conversation_history.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)
        

    with st.spinner('Please wait...'):
        #챗봇 응답 생성
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




# 대화 로그를 파일에 저장하는 함수
def save_conversation_to_file(conversation):
    with open("chat_log.csv", mode='a', newline='', encoding="utf-8") as file:
        for message in conversation:
                if message["role"]=='system':
                    continue
                file.write(f"{message['role']}: {message['content']}\n")

# 대화 종료 메시지 감지
if user_input == "대화 종료":
    save_conversation_to_file(st.session_state["conversation_history"])  

    
# SIDEBAR 관리
with st.sidebar:
    st.sidebar.header('Career Counseling Chatbot')
    st.sidebar.markdown('진로 결정 어려움을 해결하여 진로 결정을 잘할 수 있도록 도와주는 AI 진로 상담사')
    st.sidebar.link_button("Career Decision-making Difficulties Questionnaire", "https://kivunim.huji.ac.il/eng-quest/cddq_nse/cddq_nse_main.html")
    st.sidebar.button("로그 저장", on_click=save_conversation_to_file(st.session_state["conversation_history"]))



