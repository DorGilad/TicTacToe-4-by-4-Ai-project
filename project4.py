import csv
import random
import time
import numpy as np
import tensorflow as tf


class Game:
    def __init__(self):
        self.board = np.ones(16, dtype=int)  # מערך חד מימדי של המשחקון
        self.turn = 1  # כמות התורות של המשחקון
        self.board2d = np.reshape(self.board, (4, 4))  # מערך דו מימדי של המשחקון
        self.save_boards = []  # שומר את כל הלוחות של המשחקון
        self.score_board = [] # שומר את כל לוחות המשחק עם ציון שמוענק להם
        self.grades = {"lose": 1.0, "not over": 0.5, "win": 0.0} # מערך הציונים (0-הפסד, 0.5-תיקו, 1-ניצחון)
        self.gama = 0.95 # הייפרפרמטר אשר מופעל על הציון של לוחות קודמים ללוח האחרון של המשחקון
        self.model_j = self.open_model() # מכיל את הרשת נוירונים

        self.dictionary = {} # המילון של כל הלוחות ששוחקו

        # self.opendict() # פותח את המילון אשר שמור ב קובץ csv

    def opendict(self): # פותח את המילון מקובץ csv לתוך התכונה self.dictionary
        csv_filename = 'dictionary.csv'
        with open(csv_filename) as f:
            reader = csv.reader(f)
            for row in reader:
                self.dictionary[str(row[0])] = (float(row[1][1:]), int(row[2][1:len(row[2]) - 1]))

    def open_model(self):# פותח את הרשת נוירונים מקובץ jason ן h5 לתוך התכונה self.model_j
        with open('fashionmnist_model.json', 'r') as json_file:
            json_savedmodel = json_file.read()
        model_j = tf.keras.models.model_from_json(json_savedmodel)
        model_j.load_weights('fashionmnist_weights.h5')
        return model_j

    def createdatafile(self): # יוצר קובץ csv מהתכונה self.dictionary
        with open('dictionary.csv', 'w') as output_file:
            for key in self.dictionary:
                output_file.write("%s,%s\n" % (key, self.dictionary[key]))
        output_file.close()

    def check_win(self): # בודק ניצחון של השחקן (כביכול האנושי) אם הוא ניצח מחזיר won אחרת אם הפסיד מחזיר lose אחרת מחזיר not over
        # בודק שורות ועמודות
        if np.any(np.all(self.board2d == 0, axis=0)) or np.any(np.all(self.board2d == 0, axis=1)):
            return 'win'
        if np.any(np.all(self.board2d == 2, axis=0)) or np.any(np.all(self.board2d == 2, axis=1)):
            return 'lose'
        # בודק אלכסונים
        if np.all(self.board2d.diagonal() == 0) or np.all(np.fliplr(self.board2d).diagonal() == 0):
            return 'win'
        if np.all(self.board2d.diagonal() == 2) or np.all(np.fliplr(self.board2d).diagonal() == 2):
            return 'lose'
        return 'not over'

    def check_chance_to_win(self, board): # בודק האם מישהו ניצח (השחקן או המחשב - 0\2 - x\o) ומחזיר האם מישהו ניצח או לא
        # בודק שורות ועמודות
        board = np.reshape(board, (4, 4))
        if np.any(np.all(board == 0, axis=0)) or np.any(np.all(board == 0, axis=1)):
            return True
        if np.any(np.all(board == 2, axis=0)) or np.any(np.all(board == 2, axis=1)):
            return True
        # בודק אלכסונים
        if np.all(board.diagonal() == 0) or np.all(np.fliplr(board).diagonal() == 0):
            return True
        if np.all(board.diagonal() == 2) or np.all(np.fliplr(board).diagonal() == 2):
            return True
        return False

    def empty_places(self): # מחזיר מערך עם כל המקומות הריקים שנותרו בלוח המשחקון
        return list(np.where(self.board == 1)[0])

    def init_board(self): # מאפס את לוח המשחקון
        self.board = np.ones(16, dtype=int)  # מאתחל את הלוח ללוח ריק , כלומר רק אחדים
        self.board2d = np.reshape(self.board, (4, 4))  # מאתחל את הלוח המשחק הדו מימדי , כלומר רק אחדים וקושר אותו ללוח החד מימדי כך שאם הלוח החד מימדי משתנה גם הוא ישתנה

# ----------------------------------------------------------------------------

    def can_win(self, who): #  בודק האם השחקן (who) יכול לנצח אם כן מחזיר את המיקום שבו הוא יכול לנצח אם לא מחזיר -1
        current_bord = self.board.copy()
        empty = self.empty_places()
        for i in empty:
            current_bord[i] = who
            if self.check_chance_to_win(current_bord):
                return i
            current_bord = self.board.copy()
        return -1

# ----------------------------------------------------------------------------

    def order_dictionary(self): # מכניס את לוחות המשחקון לתוך המילון
        self.calculate_board()  # מנקד את לוחות המשחקונים של המשחק
        for i in self.score_board:  # לכל אורך לוחות המשחקונים של המשחק המנוקדים
            key = ''.join(map(str, i[0]))  # יוצר ממערך המשחקון מחרוזת
            if key not in self.dictionary:  # אם המחרוזת הזאת לא קיימת במילון
                self.dictionary[key] = (i[1], 1)  # יוצר מקום חדש במילון עם התוצאה של לוח המשחקון
            else:  # אם המחרוזת הזאת קיימת במילון
                self.dictionary[key] = (((self.dictionary[key][0] * self.dictionary[key][1]) + i[1]) / (self.dictionary[key][1] + 1), self.dictionary[key][1] + 1)  # מעדכן את המקום של המשחקון לפי המבוקש ( ממוצע דירוג המשחקוןנים שבהם לוח המשחקון הזה הופיע )

    def calculate_board(self): # מנקד את לוחות המשחקון
        self.score_board = []  # מאפס את ניקוד המשחק הקודם
        who_won = self.check_win()  # מחזיר את תוצאת המשחק (win/lose/not over = tie)
        self.score_board.append((self.save_boards.pop(), self.grades[who_won]))  # מוסיף את לוח המשחקון האחרון של המשחק האחרון ששוחק ללוח התוצאות ומדרג אותו לפי התוצאה (0 - הפסד , 0.5 - תיקו , 1 - ניצחון)
        for i in range(1, len(self.save_boards)):  # לאורך כל שאר הלוחות של המשחק
            self.score_board.append((self.save_boards.pop(), (self.score_board[i - 1][1] * self.gama)))  # מוסיף את לוח המשחקון ללוח התוצאות ומדרג אותו לפי לוח המשחקון שהוכנס לפניו ( הגאמא )

# ----------------------------------------------------------------------------

    def computer_turn(self): # מחזיר תא ריק ראנדומאלי
        self.turn += 1  # מוסיף תור לכמות התורות ששיחקו
        return random.choice(self.empty_places())

    def smart_computer_turn(self): # תור של מחשב חכם בשימוש במילון
        current_bord = self.board.copy()
        empty = self.empty_places()
        best_move = random.choice(empty)
        best_score = -1
        for i in empty: # עובר על כל המקומות הריקים
            current_bord[i] = 2
            key = ''.join(map(str, current_bord))
            if key in self.dictionary and self.dictionary[key][0] >= best_score: # בודק מהו הציון המקסימלי
                best_score = self.dictionary[key][0]
                best_move = i
            current_bord = self.board.copy()
        self.turn += 1
        # print(best_move, best_score)
        return best_move # מחזיר את המיקום שכי טוב למחשב לשחק

    def model_predict(self): # תור של מחשב חכם בשימוש ברשת הנוירונים
        he_can_win = self.can_win(0) # בודק האם השחקן יכול לנצח באיזה שהוא מיקום בלוח
        you_can_win = self.can_win(2) # בודק האם המחשב יכול לנצח באיזה שהוא מקום בלוח
        if he_can_win != -1 and you_can_win == -1: # אם השחקן יכול לנצח והמחשב לא יכול הוא יחסום את השחקן
            self.turn += 1
            # print("block!")
            return he_can_win
        current_bord = self.board.copy()
        empty = self.empty_places()
        best_move = random.choice(empty)
        best_score = -1
        for i in empty: # עובר על כל המקומות הריקים בלוח המשחקון
            current_bord[i] = 2
            winner = np.array(current_bord).reshape(-1, 1).T
            result = self.model_j.predict(winner, verbose=0)
            if result >= best_score: # בודק מהו הציון המקסימלי
                best_score = result
                best_move = i
            current_bord = self.board.copy()
        self.turn += 1
        # print(best_move, best_score)
        return best_move # מחזיר את המיקום שכי טוב למחשב לשחק

# ----------------------------------------------------------------------------

    def play_100000_games(self): # משחק 100000 משחקים של מחשב נגד מחשב רנדומאלי
        player1 = 0 # כמות הפעמים שמחשב1 ניצח
        player2 = 0 # כמות הפעמים שמחשב2 ניצח
        for i in range(10000): # ל מאה אלף משחקים
            score = self.play_one_game_computer() # משחק משחק אחד של מחשב נגד מחשב
            if score == 'lose':# אם מחשב1 ניצח
                player1 += 1# מוסיף ניצחון למחשב1
            elif score == "win":# אם מחשב2 ניצח
                player2 += 1# מוסיף ניצחון למחשב2

        print("סוכן: ", (player1 / 10000) * 100, "%")  # מדפיס את אחוזי הניצחון של מחשב1
        print("מחשב רנדומאלי: ", (player2 / 10000) * 100, "%")  # מדפיס את אחוזי הניצחון של מחשב2

    def play_one_game_computer(self): # משחק משחק של מחשב נגד מחשב רנדומאלי ומחזיר את תוצאת המשחק (win\lose\not over)
        self.init_board()  # מאתחל את לוחות המשחקונים
        self.save_boards = []  # מאתחל את שומר לוחות המשחקונים
        who_won = 'not over'  # שומר את תוצאת המשחקון האחרון
        self.turn = 1  # מונה את כמות התורות ששוחקו
        self.save_boards.append(self.board.copy())  # מוסיף את לוח המשחקון למערך המשחקונים
        while who_won == 'not over' and self.turn <= 16:  # כל עוד אין ניצחון והמשחק לא שוחק יותר מ - 9 תורות
            self.board[self.computer_turn()] = (self.turn % 2)*2  # משחק תור של אחד המחשבים
            self.save_boards.append(self.board.copy())  # מוסיף את לוח המשחקון למערך המשחקונים
            who_won = self.check_win()  # בודק האם מישהו ניצח
        self.order_dictionary()  # מארגן את המילון מחדש לפי הלוחות של המשחק
        return who_won  # מחזיר את תוצאת המשחק (win/lose/not over = tie)

    def play_one_game_smart_computer(self): # משחק משחק אחד של מחשב רנדומאלי נגד מחשב חכם בשימוש במילון\ברשת נוירונים ומחזיר את תוצאת המשחק(win\lose\not over)
        self.init_board() # מאתחל את לוחות המשחקונים
        self.save_boards = [] # מאתחל את שומר לוחות המשחקונים
        who_won = 'not over' # שומר את תוצאת המשחקון האחרון
        self.turn = 1 # מונה את כמות התורות ששוחקו
        self.save_boards.append(self.board.copy()) #  מוסיף את לוח המשחקון למערך המשחקונים
        while who_won == 'not over' and self.turn <= 16: # כל עוד אין ניצחון והמשחק לא שוחק יותר מ - 16 תורות
            if self.turn % 2 == 0: # אם זה תור של המחשב0
                self.board[self.computer_turn()] = 0  # המחשב0 משחק
            else: # אם זה תור של המחשב2
                self.board[self.smart_computer_turn()] = 2 # המחשב2 משחק חכם בשימוש במילון
                # self.board[self.model_predict()] = 2 # המחשב2 משחק חכם בשימוש ברשת נוירונים
            self.save_boards.append(self.board.copy()) #  מוסיף את לוח המשחקון למערך המשחקונים
            who_won = self.check_win() # בודק האם מישהו ניצח
        self.order_dictionary() # מארגן את המילון מחדש לפי הלוחות של המשחק
        return who_won # מחזיר את תוצאת המשחק (win/lose/not over = tie)

    def play_100000_smart_games(self): # משחק 100000 משחקים של מחשב חכם נגד מחשב רנדומאלי
        player1 = 0 # כמות הפעמים שמחשב1 ניצח
        player2 = 0 # כמות הפעמים שמחשב2 ניצח
        for i in range(1000): # ל מאה אלף משחקים
            if i % 100000 == 0:
                print(i)
            score = self.play_one_game_smart_computer() # שחק משחק אחד של מחשב נגד מחשב
            if score == 'lose': # אם מחשב1 ניצח
                player1 += 1 # מוסיף ניצחון למחשב1
            elif score == 'win': # אם מחשב2 ניצח
                player2 += 1 # מוסיף ניצחון למחשב2

        print("סוכן: ", (player1 / 1000) * 100, "%") # מדפיס את אחוזי הניצחון של מחשב1
        print("מחשב רנדומאלי: ", (player2 / 1000) * 100, "%") # מדפיס את אחוזי הניצחון של מחשב2

# ----------------------------------------------------------------------------
if __name__ == '__main__':
    game = Game() # יוצר את מחלקת המשחק

    start = time.time() # שומר זמן התחלתי
    game.play_100000_smart_games()
    # game.createDataFile() # יוצר את המילון
    end = time.time() - start
    print(int(end // 60), ":", int(end % 60)) # מדפיס כמה זמן לקח לקוד לרוץ
