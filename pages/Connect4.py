import time

import streamlit as st
import random

import copy
#from Helper import *

#משתנים קבועים
ROWS = 6
COLS = 7

PLAYER = "🟣"
COMPUTER = "🟡"
EMPTY = "⚪"
#setRTL()

#moves = 3
if "moves" not in st.session_state:
    st.session_state.moves = 3

with st.sidebar:
    st.text(f"שחקן: {PLAYER}")
    st.text(f"מחשב: {COMPUTER}")

    st.divider() #קו

    moves = st.slider(
        label="רמת קושי",
        min_value = 1,
        max_value=5,
        value=st.session_state.moves
    )

#איך זה עובד - בהתחלה היא מחשבת מהלך של המחשב, ואז בודקת את המהלך הבא - של השחקן עד סיום המהלכים
#ככל שיש יותר מהלכים - המחשב יותר חכם
#ההנחה של המחשב היא - שהשחקן תמיד רוצה לנצח - כלומר - השחקן תמיד יבחר את המהלך הכי גרוע למחשב
def minimax(board_copy,move_number,current_player,alpha,beta):
    print(f"נותרו {move_number} מהלכים")
    #ניקוד הלוח של כל אחד מהשחקנים
    computer_score = calc_board(board_copy,COMPUTER)
    user_score = calc_board(board_copy,PLAYER)

    big_number = 999999999
    #אם המחשב ניצח - מחזיר מספר ענק כי זה המהלך בוודאות הכי טוב
    if computer_score >= 10000:
        return big_number
    if user_score >= 10000:
        return -big_number

    all_cols = available_cols(board_copy) #איזה עמודות פנויות
    if all_cols == []:
        return 0 #תיקו - לא טוב ולא רע

    if move_number == 0: #אם נגמרו לי מהלכים קדימה לבדוק
        return computer_score #מה הציון של המחשב אחרי שבדקתי את כל המהלכים

    if current_player == COMPUTER:
        #המחשב רוצה שיהיה לו טוב
        best_score = -big_number #הכי טוב - זה ממש נמוך
        for col in all_cols: #תעבור על כל העמודות הקיימות
            new_copy_board = virtual_board(board_copy,COMPUTER,col) #מה יקרה אם לחצתי
            col_score = minimax(new_copy_board, move_number - 1,PLAYER,alpha, beta) #התור הבא - בלוח החדש - של האדם
            if best_score < col_score:
                best_score = col_score #יש לי ציון הכי טוב חדש
            if alpha < best_score:
                alpha = best_score #יש לי אופציה יותר טובה
            if alpha >= beta: #אם מצאתי משהו יותר טוב מהכי גרוע
                break #מצאת את ההכי טוב שהיריב יתן לך לעשות
        return best_score
    else:
        #המטרה של השחקן - שיהיה לא טוב למחשב
        worst_score = big_number #הכי גרוע למחשב - נתחיל מהמצב הכי טוב - וכל פעם נוריד ליותר גרוע

        for col in all_cols:
            new_copy_board = virtual_board(board_copy,PLAYER,col) #מה קרה אם השחקן לחץ
            col_score = minimax(new_copy_board, move_number - 1, COMPUTER,alpha, beta) #התור של המחשב
            if col_score < worst_score:
                worst_score = col_score
            if worst_score < beta: #אם היריב מצא מצב יותר גרוע למחשב
                beta = worst_score
            if alpha >= beta: #אם מצאתי משהו יותר טוב מהכי גרוע
                break #מצאת את ההכי טוב שהיריב יתן לך לעשות
        return worst_score



        #פונקציה - שמה באופן וירטואלי עיגול בעמודה מסויימת
#לוח - שחקן - מספר עמודה
def virtual_board(board,player,col):
    copy_board = copy.deepcopy(board) #תעתיק את הלוח
    for i in range(ROWS - 1,-1, -1): #להתחיל מהסוף להתחלה
        if copy_board[i][col] == EMPTY: #אם הוא ריק
            copy_board[i][col] = player #להפיל עד לשם
            break
    return copy_board


def get_best_col(board,player): #פונקציה שמטרתה למצוא את העמודה הכי טובה לשחקן
    valid_cols = available_cols(board) #מאיפה  אפשר לבדוק
    best_col = -1 #כרגע אין עמודה הכי טובה
    best_score = -999999999 #אין ניקוד הכי טוב

    scores = ["-"] * COLS        #[5,-,50,-,-50,-,-,-]

    for c in valid_cols: #לך על כל מספר עמודה מהעמודות שאפשר ללכת עליהן
        temp_board = virtual_board(board,player,c) #צור לוח וירטואלי
        #col_score = calc_board(temp_board,player) #חשב מה הניקוד של העמודה
        # פחות 1 - כי המהלך הראשון נעשה
        #שולחים אלפא וביטא - המצב הכי טוב והמצב הכי פחות טוב
        col_score = minimax(temp_board,moves -1, PLAYER if player==COMPUTER else COMPUTER,-99999,99999)
        scores[c] = col_score
        #אם זה הניקוד הכי טוב עכשיו
        if best_score < col_score:
            best_score = col_score
            best_col = c

    st.session_state.scores = scores  #שומר בזיכרון של הפרויקט
    return best_col #תחזיר מה הייתה העמודה הכי טובה

#לוח
def newBoard():
    board = []
    for r in range(ROWS): #עבור כל שורה
        row  = []
        for cell in range(COLS): #לכל תא בעמודה
            row.append(EMPTY) #נשים תא ריק
        board.append(row)  #להוסיף לרשימה
    return board

if "board" not in st.session_state: #לא היה לוח
    st.session_state.board = newBoard() #צור לוח ושמור בזיכרון

board = st.session_state.board #לוקח את מה ששמור
#board = newBoard() #מפעילים את הפונקציה
#r = שורה
#c = עמודה
#שחקנים
if "turn" not in st.session_state:
    st.session_state.turn = PLAYER

turn = st.session_state.turn

def switchTurn():
    if st.session_state.turn == PLAYER:
        st.session_state.turn = COMPUTER
    else:
        st.session_state.turn = PLAYER

def available_cols(board): #מקבל לוח ומחזיר    איפה פנוי
    cols = []
    for c in range(COLS): #תעבור על כל העמודות
        if board[0][c] == EMPTY: #אם יש מקום
            cols.append(c) #תוסיף את מספר העמודה לרשימת העמודות
    return cols

#פונקציה שמקבלת 4 תאים רצופים ושחקן
def calculate_score(range4,good):
    #יש לנו את השחקן - שומרים מי היריב שלו
    if good == PLAYER:
        bad = COMPUTER
    else:
        bad = PLAYER
    #ניקוד התחלתי
    score = 0

    if range4.count(good) == 4: #אם יש 4 טובים - ניצחון
        score += 50000 #ניצחון - ממש גבוה - זה המצב הכי טוב
    #3 + חור - סיכוי גבוה לנצח
    elif range4.count(good) == 3 and range4.count(EMPTY) == 1:
        score += 100
    elif range4.count(good) == 2 and range4.count(EMPTY) == 2:
        score += 10 #לא מדהים - אבל מקדם קצת

    #מצבים לא טובים
    if range4.count(bad) == 4:
        score -= 50000 #ממש לא טוב - היריב ניצח
    elif range4.count(bad) == 3 and range4.count(EMPTY) == 1:
        score -= 500 #לא טוב לי - סיכוי גבוה שהשחקן השני ינצח
    elif range4.count(bad) == 2 and range4.count(EMPTY) == 2:
        score -= 50 #קירבתי את השחקן השני לניצחון - זה קנס

    #print(range4,good,score)
    return score

#calculate_score([PLAYER,PLAYER,EMPTY,PLAYER],PLAYER)

#פונקציה - שבודקת מה הניקוד של כל הלוח
def calc_board(board,good):
    score = 0 #הניקוד של הלוח הוא 0

    for r in range(ROWS):
        row = board[r] #השורה שאנחנו עליה
        for c in range(COLS - 3): #עבור כל עמודה
            range4 = row[c:c+4] #יוצר רשימה חדשה דרך המיקומים
            score += calculate_score(range4,good)

    for c in range(COLS):
        col = [board[r][c] for r in range(ROWS)]
        for r in range(ROWS - 3):
            range4 = col[r : r + 4]
            score += calculate_score(range4,good)

    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            #יורד
            range4 = [board[r + i][c + i] for i in range(4)]
            score += calculate_score(range4,good)
            #עולה
            range4 = [board[r + 3 - i][c + i] for i in range(4)]
            score += calculate_score(range4,good)

    #ניקוד לעמודה האמצעית
    middle_col_number = COLS // 2 #חילוק בלי שארית = 3.5 - 3
    middle_col =  [board[r][middle_col_number] for r in range(ROWS)]#כל הדסקיות בעמודה האמצעית
    score += middle_col.count(good) * 5 #נתנו 5 נקודות על כל עיגול באמצע

    right_col =  [board[r][middle_col_number + 1] for r in range(ROWS)]
    score += right_col.count(good) * 2 #העמודה ליד האמצעית גם סבבה

    left_col =  [board[r][middle_col_number - 1] for r in range(ROWS)]
    score += left_col.count(good) * 2 #העמודה ליד האמצעית גם סבבה

    return score


#print(calc_board(board,turn),turn)

#פונקציה שבודקת מי והאם יש מנצח
def checkWinner(check_row, check_col):
    #שורות - לתקן - לבדוק רק את השורה הרלוונטית
    #for row in range(ROWS): #תעבור על כל שורה בלוח
    row = check_row #השורה ששלחנו
    for cell in range(COLS - 3):
        if board[row][cell] == EMPTY:
            continue #תמשיך הלאה לתא הבא בלולאה
        for i in range(cell,cell+4):
            if board[row][i] != board[row][cell]:  #אם הוא לא שווה למה שיש בתא הראשון
           #     print(f"No Win starts with row {row} cell {cell}")
                break #צא - זה לא רביעיה
        else: #האם הלולאה הסתיימה לא בגלל ברייק - הגיעה לסיום
            print("הגיעה לסיום")
            print(board[row][cell])
            return board[row][cell] #מחזירים - מי המנצח

    col = check_col #בודקים עמודות
    for cell in range(ROWS - 3): #תעבור כל שורה בעמודה
        if board[cell][col] == EMPTY:
            continue #תמשיך הלאה לתא הבא בלולאה
        for i in range(cell,cell+4):
            if board[i][col] != board[cell][col]:  #אם הוא לא שווה למה שיש בתא הראשון
             #   print(f"No Win starts with col {col} cell {cell}")
                break #צא - זה לא רביעיה
        else: #האם הלולאה הסתיימה לא בגלל ברייק - הגיעה לסיום
            print("הגיעה לסיום")
            print(board[cell][col])
            return board[cell][col] #מחזירים - מי המנצח

    #אלכסון יורד
    offset = min (check_row,check_col) #תמצא מי יותר קטן
    start_row = check_row - offset #הולכים שמאלה לפי המספר הקטן
    start_col = check_col - offset #הולכים כמה שניתן למטה

    if start_row + 4 > ROWS or start_col + 4 > COLS: #אם אין סיכוי לנצח
        print("אין ניצחון באלכסון הזה")
    else:
        count = 0 #יש 0 ברצף
        for i in range (ROWS): #מהשורה הראשונה שהגדרנו - ועד למספר השורות שקיימות
            row = start_row + i
            col = start_col + i


            #עוברים על כל האלכסון ובודקים מה הרצף
            if col == COLS or row == ROWS: #אם יצאתי ממספר העמודות או השורות
                break #צא - אף אחד לא ניצח
            elif board[row] [col] == EMPTY: #אם יש לי ריק
                count = 0 #מאפסים את הספירה
            elif board[row][col] != board[check_row][check_col]: #אם מה שיש שם - זה לא מה שהשחקן שם
                count = 0 #מאפסים את הספירה
            #אם לא ריק - ולא של היריב
            else:
                count += 1 #מוסיפים אחד לרצף
            if count == 4:
                print("ניצחון")
                print(board[row][col])
                return board[row][col]  # מחזירים - מי המנצח

    #אלכסון עולה - משמאל למטה - לימין למעלה
    dist_bottom = ROWS - 1 - check_row #מרחק מהשורה האחרונה (מתחילים מ0)
    dist_left = check_col #מרחק שמאל - מספר העמודה
    offset = min (dist_left,dist_bottom) #איזה מרחק קטן יותר - מה הקיר הראשון

    start_row = check_row + offset #יורדים למטה - זה פלוס
    start_col = check_col - offset #הולכים שמאלה - זה מינוס

    if start_row - 4 < 0 or start_col + 4 > COLS: #אם אין מקום לאלכסון
        print("אין ניצחון באלכסון הזה")
    else:
        count = 0 #יש 0 רצופים
        for i in range(ROWS): #תעבור על כל תא באלכסון
            row = start_row - i #לעלות למעלה
            col = start_col + i #ללכת ימינה
            print(f"start checking: {row} {col}")

            if col == COLS or row == ROWS or row<0:
                break #יצאתי מהלוח
            elif board[row] [col] == EMPTY: #אם יש לי ריק
                count = 0 #מאפסים את הספירה
            elif board[row][col] != board[check_row][check_col]: #אם זה השחקן השני
                count = 0
            else:
                count += 1
            if count == 4: #אם יש 4 רצופים
                print("ניצחון")
                print(board[row][col])
                return board[row][col]  # מחזירים - מי המנצח
    #בדקתי הכל - אין מנצחים
    return None #מחזיר כלום - אין מנצח


def click(col):
    #אם העמודה מלאה - אז לא להחשיב את התור
    if board[0][col] != EMPTY: #אם התא העליון בעמודה לא ריק
        return #צא מהפונקציה - לא מחשיב את התור

    #st.write(col)
    for i in range(ROWS - 1,-1,-1): #מהשורה האחרונה - עד לראשונה - בירידה
        if board[i][col] == EMPTY: #אם המקום ריק
            board[i][col] = turn #אפשר לשים בו
            st.session_state.winner = checkWinner(i,col) #שולחים לבדיקה את מספר השורה והעמודה- שומרים את התוצאה
            break
    #board[0][col] = PLAYER
    st.session_state.board = board #מעדכנים

    switchTurn()
    st.rerun() #כדי שנראה את השינויים

def computerTurn():
    time.sleep(1) #בינתיים - שירגיש כאילו לוקח לו זמן לחשוב
    #randomCol = random.randint(0,COLS-1) #תגריל עמודה
    #click(randomCol)
    best_col = get_best_col(board,COMPUTER) #תמצא מה העמודה הכי טובה למחשב
    click(best_col)

# if turn == COMPUTER:
#     computerTurn() #תפעיל תור של המחשב
winner = None #אין מנצח
if "winner" in st.session_state: #אם שמור מנצח כלשהו
    winner = st.session_state.winner

can_play = True #לרוב אפשר לשחק


#print(available_cols(board))

def resetGame():
    if st.button("משחק חדש"): #אם לחצתי על כפתור משחק חדש
        st.session_state.winner = None #אין מנצח
        st.session_state.scores = [0] * COLS #אין ניקוד
        st.session_state.board = newBoard() #לוח חדש
        st.session_state.turn = PLAYER #תור שחקן
        st.rerun() #להפעיל מחדש


if winner == PLAYER:
    st.info("השחקן ניצח!")
    can_play = False
    resetGame()
    st.balloons()
elif winner == COMPUTER:
    st.info("המחשב ניצח")
    can_play = False
    resetGame()
elif available_cols(board) == []:
    st.info("תיקו")
    can_play = False
    resetGame()
else: #מציג תורות רק אם לא השחקן ולא המחשב ניצחו
    if turn == PLAYER:
        st.info("עכשיו תור השחקן")
    else:
        st.status("המחשב חושב")

if "scores" not in st.session_state: #אם לא היה ניקודים
    st.session_state.scores = [0] * COLS

scores = st.session_state.scores
print(scores)

#ליצור את הלוח
for r in range(ROWS): #תעבור כל שורה
    columns = st.columns(COLS) #צור לפי מספר העמודות שהגדרתי - שורה מחולקת
    #לשים תוכן בתאים שנוצרו
    for c in range(COLS): #תעבור על כל עמודה - לפי מספר העמודות שיש לי
        with columns[c]: #בתוך העמודה הנוכחית
            cell = board[r][c] #תא - הלוח בשורה עכשיו, העמודה העכשיו
            if st.button(cell, #צור כפתור עם מה שיש בתא
                      key= f"row_{r}_col_{c}", #מזהה ייחודי
                      use_container_width=True,
                      disabled = turn==COMPUTER or not can_play   ): #לא פעיל אם התור של המחשב
               click(c) #מגדירים שלחצנו על העמודה

columns = st.columns(COLS) #עוד שורה מחולקת
for c in range(COLS): #עבור כל עמודה
    with columns[c]: #בתוך מספר העמודה
        col_score = scores[c] #מה הניקוד של העמודה
        if col_score == 0 or col_score == '-':
            st.badge(str(col_score),color="gray")
        elif col_score < 0:
            st.badge(str(col_score),color="red")
        else:
            st.badge(str(col_score),color="green")

#בסוף - כדי שקודם יצור את הלוח ואז ישים
if turn == COMPUTER and can_play:
    computerTurn() #תפעיל תור של המחשב
