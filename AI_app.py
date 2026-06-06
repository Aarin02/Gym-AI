# AI_app.py

import streamlit as st
import google.generativeai as genai

gemini_API_KEY=st.secrets["gemini_API"]

genai.configure(api_key=gemini_API_KEY)
model = genai.GenerativeModel("gemini-3.5-flash")

ins=["INSTRUCTION= You are a supportive,enthusiastic, straight to the point gym instructor and nutritionist, you have been tasked to guide people with anything gym or nutrition related, you must refuse to answer anything thats not related to gym and nutrition, answer should be short,crisp and straightforward, format your answer in such a way that its easily readable and feels like human. Use emojis ever so slightly"]

st.set_page_config(page_title="Gym *AI*")
st.title("Gym:red[AI]")

if "instruction" not in st.session_state:
  st.session_state.instruction=[ins]
if "conversation" not in st.session_state:
  st.session_state.conversation=[]

user_input = st.bottom.chat_input("Ask GymAI",key="user_input")

if user_input!=None:
  st.session_state.conversation.append({{"role":"user","parts":[user_input]}})

  context=st.session_state.conversation[-6:]
  instruction=st.session_state.instruction[-1]

  try:
    with st.bottom.spinner("Gym:red[AI] is thinking..."):
      response = model.generate_content(str(instruction + context))
      clean_text = response.text.replace('*', '')
      reply = clean_text
  except Exception as e:
    reply = f"Error: {{str(e)}}"

  st.session_state.conversation.append({{"role": "model", "parts": [reply]}})

for message in st.session_state.conversation:
  if message["role"] == "user":
    st.chat_message("user").write(f"{{message['parts'][0]}}")
  elif message["role"] == "model":
    st.chat_message("ai").write(f"{{message['parts'][0]}}")
