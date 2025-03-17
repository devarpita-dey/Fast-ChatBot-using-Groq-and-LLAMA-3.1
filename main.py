import os
import json

import streamlit as st
from groq import Groq

#streamlit page configuration
st.set_page_config(
    page_title="LLAMA 3.1 Chat",
    page_icon="🦙",
    layout="centered"
)

working_dir= os.path.dirname(os.path.abspath(__file__))   # absolute path of the main automatically without any specific directory mentioned
config_data= json.load(open(f"{working_dir}/config.json")) # working directory because streamlit may run from a different directory

GROQ_API_KEY= config_data["GROQ_API_KEY"]

#save the api key to the environment variable
os.environ["GROQ_API_KEY"]=GROQ_API_KEY


client =Groq()


#initialize the chat history as streamlit session state of not present already

if 'chat_history' not in st.session_state:
    st.session_state.chat_history=[]


#streamlit page tittle
st.title("🦙LLAMA 3.1 Chat Bot")


#display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])



#input field for user's message
user_prompt=st.chat_input("Ask Llama...")

if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role":"user", "content": user_prompt})

    #send user's message to the LLM and get a response

    messages = [
    {"role": "system", "content": "You are a helpful assistant"}
    ] + st.session_state.chat_history
    
    response= client.chat.completions.create(
        model= "llama3-8b-8192",
        messages=messages
    )

    assistant_response= response.choices[0].message.content
    st.session_state.chat_history.append({"role":"assistant", "content": assistant_response})

    #display the LLM's response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
