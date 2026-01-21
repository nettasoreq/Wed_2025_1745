import streamlit as st
from Helper import * #תטען את קובץ ההלפר

st.set_page_config(
    page_title="בוט שיעורי בית",
    page_icon="🤓",
)

setRTL() #יישור לימין - לוקחים מדף ההלפר

st.title("בוט שיעורי בית")

API_KEY = getAPIkey()

#פה יהיה פרומפט

Message("AI","היי איך אפשר לעזור לך")

userinput = st.chat_input("השאלה שלך...")

if userinput: #אם כתבתי הודעה
    Message("User",userinput)
    sendMessage(userinput)




