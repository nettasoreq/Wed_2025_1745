import streamlit as st
from Helper import *  # תטען את קובץ ההלפר
import PIL.Image  # ספריה של תמונות


st.set_page_config(
    page_title="סוכן קוד",
    page_icon="🤓",
)




setRTL()  # יישור לימין - לוקחים מדף ההלפר

newPage("CodeAgent")

st.title("סוכן קוד")

API_KEY = getAPIkey()

# הוראות איך לפעול
systemPrompt = """
    ## תפקיד
    אתה מומחה-על לתכנות ופיתוח תוכנה. תפקידך להוביל את המשתמש צעד אחר צעד (לפי שלבי העבודה המוגדרים) משלב הרעיון ועד לקוד מלא, עובד ואיכותי.
    
    ## זרימת העבודה (שלב אחר שלב)
    אתה עובד אך ורק לפי שלבי העבודה הבאים. אל תדלג על שלבים!
    1. **בחירת נושא (idea)**: הבנת הרעיון הכללי. אם למשתמש אין רעיון, הצע לו 3 רעיונות יצירתיים.
    2. **שאלות הבהרה (question)**: שאל שאלות ממוקדות כדי להבין את הטכנולוגיה, קהל היעד והדרישות.
    3. **תוכנית (plan)**: יצירת אפיון ותוכנית ארכיטקטורה כללית לפרויקט.
    4. **שלבי פיתוח (development_plan)**: פירוק הפרויקט למשימות קטנות וברורות (שלב 1, שלב 2 וכו').
    5. **כתיבת קוד (code)**: כתיבת הקוד עצמו, חלק אחר חלק, עם הסברים מפורטים והערות.
    6. **בדיקות (check)**: בדיקת הקוד ומציאת באגים.
    
    ---
    
    ## חוקים והנחיות פעולה (קריטי!)
    
    1. **תקשורת אינטראקטיבית ונעימה**: 
       * תענה תמיד בעברית רהוטה, נעימה ומקצועית.
       * הוסף הערות מפורטות לכל קוד שאתה כותב והסבר את הלוגיקה שלו.
       * אם יש בקוד סיכון אבטחתי או פגיעה בביצועים - התרע על כך מראש ושאל את המשתמש לאישור.
    
    2. **שימוש בכלי השאלות (`ask_question`)**:
       * כאשר חסר לך מידע או שאתה רוצה שהמשתמש יבחר אפשרות, **חובה להשתמש בכלי `ask_question`**.
       * שלח שאלה אחת ממוקדת בכל פעם עם 2-4 אפשרויות לבחירה.
       * **שים לב:** מיד לאחר הפעלת הכלי, כתוב למשתמש הודעה קצרה וידידותית שמסבירה מה שאלת ומדוע (למשל: "כדי להתקדם, אשמח אם תענה על השאלה הבאה:"). *אל תשאיר את התשובה שלך ריקה מטקסט!*
    
    3. **סיום שלב ומעבר שלבים (`mark_step_done`)**:
       * ברגע שהגעת להסכמה עם המשתמש על סיום השלב הנוכחי (למשל, יש רעיון מוסכם, או שהמשתמש אישר את תוכנית העבודה), **חובה להפעיל מיד את הכלי `mark_step_done`**.
       * שלח לכלי את שם השלב שהסתיים, סיכום קצר מאוד שלו, ואת שם השלב הבא.
       * **שים לב:** מיד לאחר הפעלת הכלי, כתוב למשתמש הודעה חגיגית שמסכמת את המעבר ומציגה את הצעד הבא (למשל: "מעולה! סיימנו את שלב X ועדכנתי את המערכת. כעת נעבור לשלב Y..."). *אל תעצור את השיחה ואל תחזיר תשובה ריקה!*
"""

steps = {
    "idea":"בחירת נושא",
    "question": "שאלות הבהרה",
    "plan" : "תוכנית",
    "development_plan": "שלבי פיתוח",
    "code":"כתיבת קוד",
    "check": "בדיקות"
}


if "completed_steps" not in st.session_state:
    st.session_state.completed_steps = []
if "current_step" not in st.session_state:
    st.session_state.current_step = "idea"

if ask_question not in tools:
    tools.append(ask_question)

if mark_step_done not in tools:
    tools.append(mark_step_done)

updated_prompt = f"""
                    שלבי עבודה: {steps},
                    השלבים שהושלמו: {st.session_state.completed_steps}
                    השלב הנוכחי: {st.session_state.current_step}
                """
st.session_state.system_prompt = systemPrompt + updated_prompt  # שומרים בזיכרון
#print(st.session_state.system_prompt)
with st.sidebar:
    st.write("**שלבי העבודה**")
    for step in steps:
        if step in st.session_state.completed_steps:
            st.badge(steps[step],color="green",icon="✅")
        elif step == st.session_state.current_step:
            st.badge(steps[step],color="blue",icon="⭐")
        else: #לא עשינו ולא נוכחי
            st.badge(steps[step],color="gray")



#משתנים בזיכרון
if "chosen_idea" not in st.session_state:
    st.session_state.chosen_idea = ""
if "plan" not in st.session_state:
    st.session_state.plan = ""
if "code_parts" not in st.session_state:
    st.session_state.code_parts = [] #רשימת חלקים

# פה יהיה פרומפט

Message("AI", "היי מה ניצור היום ביחד?")

# להציג את ההיסטוריה
for m in st.session_state.history:  # עבור כל הודעה בהיסטוריה
    Message(m["role"], m["text"])


if "status" not in st.session_state:
    st.session_state.status = "chat"

if st.session_state.status == "wait for answer":
    question = st.session_state.question
    options = st.session_state.options
    with st.chat_message("ai"):
        st.write(f"**{question}**")
        cols =  st.columns(len(options)) #צור עמודות כמספר התשובות
        for i in range(len(cols)): #עבור כל תשובה
            with cols[i]: #בעמודה
                if st.button(options[i],key=f"o_{i}"): #יוצרים כפתור
                    #print (options[i)
                    Message("User",options[i]) #מראים מה בחרתי
                    st.session_state.status = "chat" #חוזר להיות צ׳אט
                    with st.spinner("חושב..."):
                        sendMessage(options[i]) #שולח לו את ההודעה

userinput = st.chat_input("השאלה שלך...")

#image_input = st.file_uploader("העלאת תמונה", type=["jpg", "png", "jpeg"])

if userinput:  # אם כתבתי הודעה

    # בדיקה אם הייתה תמונה
    image = None
 #   if image_input:  # אם הייתה תמונה
  #      image = PIL.Image.open(image_input)  # טוען את התמונה בדרך שהספריה מכירה
   #     print(image)

    Message("User", userinput)
    with st.spinner("חושב..."):
        sendMessage(userinput)




