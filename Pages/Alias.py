import os  # Operating System - פונה למערכת ההפעלה של המחשב
from dotenv import load_dotenv  # הספריה שהורדנו - של משתני הסביבה
from google import genai  # generative ai = בינה מלאכותית יוצרת
import streamlit as st  # ספריה של ממשקים GUI

# הגדרות
st.set_page_config(
    page_title="משחק אליאס מול AI",
    page_icon='🤖'
)


st.title("משחק אליאס")



load_dotenv()  # טוענים את המשתנים
API_KEY = os.getenv("API_KEY")  # פונים לקובץ env - ומבקשים את המשתנה API_KEY


# print(API_KEY)

# seesion -  הזמן שלנו כרגע באפליקציה - מהרגע שנכנסתי ועד שיצאתי אני בסשיין אחד

def start():  # פעם ראשונה שנכנסנו
    st.session_state.end = False  # המשחק לא נגמר
    st.session_state.gemini = genai.Client(api_key=API_KEY)  # מתחברים עם הסיסמה שלנו
    st.session_state.history = []  # איפוס להיסטוריה
    message = send(prompt)  # שולחים לפונקציה

    # st.text(message)
    # תיבת טקסט של צאט


#  ai_text  = st.chat_message("ai")
#  ai_text.write(message)


# gemini = genai.Client(api_key=API_KEY) #

# הוראה -
prompt = """
    ###הקשר
    אנחנו במשחק "אליאס" - שזה משחק ניחושים
    עליך להגריל מילה ואני צריכה לנחש מה המילה שהגרלת
    אתה צריך לתת לי רמזים

    ###חוקים
    אסור שהמילה או השורש שלה יופיעו
    אל תגלה לי את המילה!
    כל פעם תן רמז אחד - הראשון יהיה כללי מאוד ואחר כך יותר ספציפי

    ###סיום משחק
    לאחר 3 נסיונות או הצלחה
    כתוב את המילה שהגרלת
    כתוב בסיום END
"""

# מודלים
all_models = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-2.5-flash-lite", "gemini-2.0-flash-lite"]


def send(prompt):
    st.session_state.loading = True  # האם כרגע טוען
    st.session_state.history.append({  # שמירה של ההודעה של היוזר
        "sender": "user",
        "text": prompt
    })
    context = "זו השיחה המלאה: \n"
    for line in st.session_state.history:  # עבור כל שורה בהיסטוריה של הצ'אט
        context += f"{line['sender']}: {line['text']}\n"  # תוסיף למשתנה

    with st.spinner("חושב..."):
        for model in all_models:  # עובר על כל מודל ברשימה
            print(model)
            chat = st.session_state.gemini.chats.create(model=model)  # לוקחים מסשיין את מה ששמור שם
            try:  # לנסות
                message = chat.send_message(context)  # שולחים
                st.session_state.history.append({  # שמירה של ההודעה של הAI
                    "sender": "ai",
                    "text": message.text
                })
                st.session_state.loading = False  # האם כרגע טוען
                # print(st.session_state.history)
                return message.text  # הצלחת לשלוח? תחזיר את התשובה
            except:  # אם לא הצליח
                print("לא הצליח - מנסה את המודל הבא")


if "gemini" not in st.session_state:  # אם אין לך ג'מיני
    start()  # תפעיל את ההתחלה

# אם זאת לא השיחה הראשונה
if 'history' in st.session_state and len(st.session_state.history) > 0:  # אם יש היסטוריה - תכתוב
    for line in st.session_state.history[1:]:  # תתחיל ממקום מספר 1 - שזו ההודעה השניה
        chat = st.chat_message(line["sender"])
        chat.write(line["text"])

if 'end' in st.session_state and st.session_state.end:  # אם המשחק נגמר
    st.balloons()
    st.success("המשחק הסתיים")

else:  # אם לא נגמר המשחק
    user = st.chat_input("ניחוש")
    if user:  # אם המשתמש ניחש
        # נכתוב את הניחוש על המסך
        user_text = st.chat_message("user")
        user_text.write(user)

        ai = send("הניחוש שלי: " + user)
        ai_text = st.chat_message("ai")
        ai_text.write(ai)

        # נגמר המשחק
        if 'END' in ai:  # אם היה END בתשובה
            st.session_state.end = True  # נגמר המשחק
            st.rerun()  # רענון