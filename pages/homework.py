import streamlit as st
from Helper import * #תטען את קובץ ההלפר
import PIL.Image #ספריה של תמונות

st.set_page_config(
    page_title="בוט שיעורי בית",
    page_icon="🤓",
)


setRTL() #יישור לימין - לוקחים מדף ההלפר

newPage("homework")

st.title("בוט שיעורי בית")

API_KEY = getAPIkey()

#הוראות איך לפעול
systemPrompt = """
    #תפקיד
    אתה בוט שיעורי בית
    
    #משימה
    המשימה שלך - לעזור לי בשיעורי בית
    תסביר ברור
    תכוון אותי לתשובה הנכונה
    
    #מגבלות
    אם אתה לא יודע - תחפש בגוגל
   **אל תמציא תשובה**
    ענה כמו בן אדם - בצורה אנושית
    
    ** אם השתמשת בכלי (Tool) תכתוב את התוצאה **
    **אנחנו בשנת 2026**
"""


st.session_state.system_prompt = systemPrompt #שומרים בזיכרון

#פה יהיה פרומפט

Message("AI","היי איך אפשר לעזור לך")

# להציג את ההיסטוריה
for m in st.session_state.history: #עבור כל הודעה בהיסטוריה
    Message(m["role"],m["text"])

userinput = st.chat_input("השאלה שלך...")


image_input = st.file_uploader("העלאת תמונה", type=["jpg","png","jpeg"])

if userinput: #אם כתבתי הודעה

    #בדיקה אם הייתה תמונה
    image = None
    if image_input: #אם הייתה תמונה
        image = PIL.Image.open(image_input) #טוען את התמונה בדרך שהספריה מכירה
        print(image)

    Message("User",userinput)
    with st.spinner("חושב..."):
        sendMessage(userinput, image)




