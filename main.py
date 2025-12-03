import streamlit as st

st.set_page_config(
    page_title="הפרויקטים של נטע",
    page_icon="👑",
    layout="wide"
)

# עיצוב כללי לימין + הסתרת תפריטים
st.markdown("""
<style>
html, body, [class*="css"] {
    direction: rtl;
    text-align: right;
    font-family: "Segoe UI", sans-serif;
}
</style>
""", unsafe_allow_html=True)


st.title("👑 הפרויקטים של נטע")
st.subheader("היי! אני נטע, מתכנתת שאוהבת ליצור דברים מגניבים 💻")
st.markdown("---")


st.header("אלה הפרויקטים שלי: ")

# 🎯 כאן משתמשים ב-st.page_link
# Streamlit אוטומטית מזהה את הדפים מהתיקייה pages/
st.page_link("pages/Alias.py", label="🎲 משחק אליאס", icon="🎮")
#st.page_link("pages/AnotherPage.py", label="🚀 פרויקט נוסף", icon="✨")
#st.page_link("pages/Contact.py", label="📬 צור קשר", icon="📧")
