import time

from dotenv import load_dotenv
import os
import streamlit as st
from google import genai  # generative ai = בינה מלאכותית יוצרת
from google.genai import types  #מאפשר להגדיר תפקידים של רכיבים שנשלחים לג'מיני

st.session_state.page = "" #באיזה דף אני
def newPage(pagename): #פונקציה שבודקת האם החלפתי דף
    if st.session_state.page != pagename:  #האם התחלף הדף
        print("דף חדש")
        st.session_state.page = pagename #שומרים אם השם של הדף החדש
        st.session_state.history = [] #מאפסים את ההיסטוריה


all_models = [
    "gemini-2.5-flash-lite",
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-3-flash",
    "gemini-2.0-flash-lite"]

#st.session_state - הזיכרון של האפליקציה
def create_chat(model,instruction,history=[]):  #מקבל מודל והיסטוריה - לרוב ריקה
    if "client" not in st.session_state: #אם אין קליינט בזיכרון
        st.session_state.client = genai.Client(api_key=getAPIkey()) #יוצר קליינט עם הAPI Key
    if instruction == "": #אם אין הוראות
        if "system_prompt" in st.session_state: #תבדוק האם הגדרנו פרומפט
            instruction = st.session_state.system_prompt
    #print(instruction)
    st.session_state.chat  = st.session_state.client.chats.create(
        model = model,
        history= history,
        config = types.GenerateContentConfig(
            system_instruction = instruction  #ההוראות לג'מיני
        )
    ) #יוצרים צ'אט במודל ששלחנו

st.session_state.modelIndex = 0 #מתחילים מהמודל הראשון

maxTrys = 5 #עד 5 נסיונות
currentTry = 0 #לא ניסינו

if  "history" not in st.session_state: #אם אין היסטוריה - ליצור
    st.session_state.history = []


def sendMessage(prompt): #פונקציה ששולחת הודעה
    #שומרים את ההודעה בהיסטוריה
    st.session_state.history.append(
        {
            "role" : "user",
            "text" : prompt
        }
    )
    if  "chat" not in st.session_state: #אם אין צ'אט - צור
        create_chat(all_models[0],"")
    global currentTry
    print(all_models[st.session_state.modelIndex])
  #  st.caption(all_models[st.session_state.modelIndex])
    try: #תנסה
        answer =  st.session_state.chat.send_message(prompt) #שולחים
        st.session_state.history.append(
            {
                "role": "model",
                "text": answer.text
            }
        )
        Message("ai",answer.text)
        currentTry = 0 #איפוס
        #אם הוא הצליח - נמשיך מפה
    except Exception as e: #אם לא הצליח
        error = str(e) #תהפוך לטקסט
        print(e)
        currentTry += 1
        if currentTry == maxTrys: #אם נגמרו הניסיונות
            st.error("תקלה - כל המודלים לא עובדים היום")
            return
        if "overloaded" in error.lower(): #תבדוק האם מופיע שהסיבה היא שהמודל עמוס
            newChat(prompt)
            # st.session_state.modelIndex +=1 #תוסיף 1 למספר המודלים
            # if st.session_state.modelIndex == len(all_models): #אם נגמרו המודלים - תחזור לראשון
            #     st.session_state.modelIndex = 0 #חוזר להיות 0
            # newmodel = all_models[st.session_state.modelIndex]
            # st.info (f"trying {newmodel}")
            # create_chat(newmodel,"") #צור צ'אט חדש
            # sendMessage(prompt) #תשלח את ההודעה
        if "429" in error: #אם קיבלנו שגיאה של יותר מדי קריאות
            with st.spinner("יותר מדי קריאות - מחכים דקה...", show_time=True):
                time.sleep(60)
                newChat(prompt)
def newChat(prompt):
    st.session_state.modelIndex += 1  # תוסיף 1 למספר המודלים
    if st.session_state.modelIndex == len(all_models):  # אם נגמרו המודלים - תחזור לראשון
        st.session_state.modelIndex = 0  # חוזר להיות 0
    newmodel = all_models[st.session_state.modelIndex]
    st.info(f"trying {newmodel}")
    create_chat(newmodel, "")  # צור צ'אט חדש
    sendMessage(prompt)  # תשלח את ההודעה


#פונקציה שטוענת את הAPI KEY ומחזירה אותו
def getAPIkey():
    load_dotenv()
    API_KEY = os.getenv("API_KEY") or st.secrets["API_KEY"] #אם לא מצאת - חפש מה ששמור אצלך בסודות של הסטרימליט
    return API_KEY


def setRTL():
    st.markdown("""
    <style>
    html, body, [class*="css"] {
        direction: rtl;
        text-align: right;
    }
    </style>
    """, unsafe_allow_html=True)




#אובייקט "שולח" - מי שלח, מה ההודעה, אייקון להודעה
class Message:
    def __init__(self,role,text): #פונקציית הבניה  - self  - מי שיצרתי
        if role.lower() == "model": #אם קוראים לו מודל - שיהיה כתוב AI
            role = "ai" #כי ככה סטרימליט אוהב
        self.role = role #מי שלח את ההודעה
        self.text = text #מה הוא שלח
        self.showMessage() #תציג את ההודעה

    def showMessage(self):
        message = st.chat_message(self.role)
        message.write(self.text)







