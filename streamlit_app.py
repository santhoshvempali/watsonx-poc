import streamlit as st
# from llama_index import VectorStoreIndex, ServiceContext, Document
# from llama_index.llms import OpenAI
# import openai
# from llama_index import SimpleDirectoryReader

from simplet5 import SimpleT5

model = SimpleT5()
model.load_model("t5","outputs/simplet5-epoch-2-train-loss-2.5781-val-loss-2.669", use_gpu=False)


st.set_page_config(page_title="HDFC CHATBOT", page_icon="🦙", layout="centered", initial_sidebar_state="auto", menu_items=None)
st.title("Chat with the  HDFC CHAT BOT, powered by T5 llm 💬🦙")
 
if "messages" not in st.session_state.keys(): # Initialize the chat messages history
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me a question about HDFC Bank!"}
    ]
if not st.session_state.get('started'):
    if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = model.predict("question:"+prompt)
            st.write(response[0])
            message = {"role": "assistant", "content": response[0]}
            st.session_state.messages.append(message) # Add response to message history



# openai.api_key = st.secrets["OPENAI_API_KEY"]

# if "openai_model" not in st.session_state:
#     st.session_state["openai_model"] = "gpt-3.5-turbo"

# if "messages" not in st.session_state:
#     st.session_state.messages = []

# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# if prompt := st.chat_input("What is up?"):
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     with st.chat_message("user"):
#         st.markdown(prompt)
        
        
    

#     with st.chat_message("assistant"):
#         message_placeholder = st.empty()
#         full_response = ""
#         for response in model.predict("question:"+prompt):
#             full_response += response
#             message_placeholder.markdown(full_response + "▌")
#         message_placeholder.markdown(full_response)
#     st.session_state.messages.append({"role": "assistant", "content": full_response})
            
    