import streamlit as st
from Helper import * #תטען את קובץ ההלפר

st.set_page_config(
    page_title="בוט שיעורי בית",
    page_icon="🤓",
)

setRTL() #יישור לימין - לוקחים מדף ההלפר

st.title("בוט שיעורי בית")

API_KEY = getAPIkey()

#הוראות איך לפעול
systemPrompt = """
   ##תפקיד
   אתה עוזר בשיעורי בית
   
   ##משימה
   אתה צריך לוודא שהמידע תקין ונכון
   נסה לכוון אותי לתשובה הנכונה
   תסביר מה התוכן

    ##מגבלות
    אם אתה לא יודע - תגיד "לא יודע" ואל תמציא
    אם לא הבנת את השאלה - תגיד "לא הבנתי"
    תנסח כמו בן אדם
"""

st.session_state.system_prompt = systemPrompt #שומרים בזיכרון

#פה יהיה פרומפט

Message("AI","היי איך אפשר לעזור לך")

# להציג את ההיסטוריה
for m in st.session_state.history: #עבור כל הודעה בהיסטוריה
    Message(m["role"],m["text"])

userinput = st.chat_input("השאלה שלך...")

if userinput: #אם כתבתי הודעה
    Message("User",userinput)
    sendMessage(userinput)




