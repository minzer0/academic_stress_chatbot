from openai import OpenAI
import streamlit as st


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
        {"role": "assistant", "content": "안녕! 나는 모니라고 해😊"}
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


# Previous conversation
CSV_FILE = "chat_history.csv"
try:
    chat_history_df = pd.read_csv(CSV_FILE)
except FileNotFoundError:
    chat_history_df = pd.DataFrame(columns=["ChatID", "Role", "Content"])


def get_button_label(chat_df, chat_id):
    first_message = chat_df[(chat_df["ChatID"] == chat_id) & (chat_df["Role"] == "User")].iloc[0]["Content"]
    return f"Chat {chat_id[0:7]}: {' '.join(first_message.split()[:5])}..."


for chat_id in chat_history_df["ChatID"].unique():
    button_label = get_button_label(chat_history_df, chat_id)
    if st.sidebar.button(button_label):
        current_chat_id = chat_id
        loaded_chat = chat_history_df[chat_history_df["ChatID"] == chat_id]
        loaded_chat_string = "\n".join(f"{row['Role']}: {row['Content']}" for _, row in loaded_chat.iterrows())
        st.text_area("이전 대화 기록 확인하기", value=loaded_chat_string, height=300)

    
# # Sidber
# with st.sidebar:
#     st.sidebar.header('이전 대화 기록 확인하기')
#     st.sidebar.button("로그 저장", on_click=save_conversation_to_file(st.session_state["conversation_history"]))


