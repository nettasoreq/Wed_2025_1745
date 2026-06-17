import streamlit as st

st.set_page_config(
    page_title="הפרויקטים של נטע",
    page_icon="👑",
    layout="wide"
)



st.title("👑 הפרויקטים של נטע")
st.subheader("היי! אני נטע, מתכנתת שאוהבת ליצור דברים מגניבים 💻")
st.markdown("---")


st.header("אלה הפרויקטים שלי: ")

# 🎯 כאן משתמשים ב-st.page_link
# Streamlit אוטומטית מזהה את הדפים מהתיקייה pages/
st.page_link("pages/Alias.py", label=" משחק אליאס", icon="🎮")
st.page_link("pages/homework.py", label=" בוט שיעורי בית", icon="🤓")
st.page_link("pages/Connect4.py", label=" ארבע בשורה מול המחשב", icon="🎲")
