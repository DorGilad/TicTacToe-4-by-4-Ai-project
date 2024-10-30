import csv
import random
import time
import numpy as np
import tensorflow as tf


class Game:
    def __init__(self):
        self.board = np.ones(16, dtype=int)  # 1D game array
        self.turn = 1  # Game turn counter
        self.board2d = np.reshape(self.board, (4, 4))  # 2D game array
        self.save_boards = []  # Stores all game boards
        self.score_board = []  # Stores all boards with assigned scores
        self.grades = {"lose": 1.0, "not over": 0.5, "win": 0.0}  # Scoring system (0-loss, 0.5-draw, 1-win)
        self.gama = 0.95  # Hyperparameter for adjusting scores of previous boards to the last game board
        self.model_j = self.open_model()  # Neural network model

        self.dictionary = {}  # Dictionary of all played boards

        # self.opendict()  # Opens the dictionary stored in a CSV file

    def opendict(self):  # Opens the dictionary from a CSV file into the self.dictionary attribute
        csv_filename = 'dictionary.csv'
        with open(csv_filename) as f:
            reader = csv.reader(f)
            for row in reader:
                self.dictionary[str(row[0])] = (float(row[1][1:]), int(row[2][1:len(row[2]) - 1]))

    def open_model(self):  # Opens the neural network model from a JSON and H5 file into the self.model_j attribute
        with open('fashionmnist_model.json', 'r') as json_file:
            json_savedmodel = json_file.read()
        model_j = tf.keras.models.model_from_json(json_savedmodel)
        model_j.load_weights('fashionmnist_weights.h5')
        return model_j

    def createdatafile(self):  # Creates a CSV file from the self.dictionary attribute
        with open('dictionary.csv', 'w') as output_file:
            for key in self.dictionary:
                output_file.write("%s,%s\n" % (key, self.dictionary[key]))
        output_file.close()

    def check_win(self):  # Checks if the player (simulated) won; returns "won" if won, "lose" if lost, otherwise "not over"
        # Checks rows and columns
        if np.any(np.all(self.board2d == 0, axis=0)) or np.any(np.all(self.board2d == 0, axis=1)):
            return 'win'
        if np.any(np.all(self.board2d == 2, axis=0)) or np.any(np.all(self.board2d == 2, axis=1)):
            return 'lose'
        # Checks diagonals
        if np.all(self.board2d.diagonal() == 0) or np.all(np.fliplr(self.board2d).diagonal() == 0):
            return 'win'
        if np.all(self.board2d.diagonal() == 2) or np.all(np.fliplr(self.board2d).diagonal() == 2):
            return 'lose'
        return 'not over'

    def check_chance_to_win(self, board):  # Checks if either player won (0 or 2 for X or O) and returns if anyone has won
        # Checks rows and columns
        board = np.reshape(board, (4, 4))
        if np.any(np.all(board == 0, axis=0)) or np.any(np.all(board == 0, axis=1)):
            return True
        if np.any(np.all(board == 2, axis=0)) or np.any(np.all(board == 2, axis=1)):
            return True
        # Checks diagonals
        if np.all(board.diagonal() == 0) or np.all(np.fliplr(board).diagonal() == 0):
            return True
        if np.all(board.diagonal() == 2) or np.all(np.fliplr(board).diagonal() == 2):
            return True
        return False

    def empty_places(self):  # Returns an array with all the remaining empty spots on the game board
        return list(np.where(self.board == 1)[0])

    def init_board(self):  # Resets the game board
        self.board = np.ones(16, dtype=int)  # Initializes the board to be empty (all ones)
        self.board2d = np.reshape(self.board, (4, 4))  # Initializes the 2D game board to be empty and links it to the 1D board

    # ----------------------------------------------------------------------------

    def can_win(self, who):  # Checks if the player (who) can win; if yes, returns the winning position, otherwise returns -1
        current_board = self.board.copy()
        empty = self.empty_places()
        for i in empty:
            current_board[i] = who
            if self.check_chance_to_win(current_board):
                return i
            current_board = self.board.copy()
        return -1

    # ----------------------------------------------------------------------------

    def order_dictionary(self):  # Inserts game boards into the dictionary
        self.calculate_board()  # Scores the boards from the game
        for i in self.score_board:  # For each board with scores in the game
            key = ''.join(map(str, i[0]))  # Converts the game board array to a string
            if key not in self.dictionary:  # If this board is not in the dictionary
                self.dictionary[key] = (i[1], 1)  # Creates a new entry with the score for the game board
            else:  # If this board is already in the dictionary
                self.dictionary[key] = (((self.dictionary[key][0] * self.dictionary[key][1]) + i[1]) / (self.dictionary[key][1] + 1), self.dictionary[key][1] + 1)  # Updates the entry with the average score for this game board

    def calculate_board(self):  # Scores the boards from the game
        self.score_board = []  # Resets previous game scores
        who_won = self.check_win()  # Gets the game result (win/lose/not over = tie)
        self.score_board.append((self.save_boards.pop(), self.grades[who_won]))  # Adds the last board and scores it based on the game result (0 - loss, 0.5 - draw, 1 - win)
        for i in range(1, len(self.save_boards)):  # For the remaining boards in the game
            self.score_board.append((self.save_boards.pop(), (self.score_board[i - 1][1] * self.gama)))  # Adds each board and scores it based on the previous board (using gamma)

    # ----------------------------------------------------------------------------

    def computer_turn(self):  # Returns a random empty cell
        self.turn += 1  # Adds to the turn count
        return random.choice(self.empty_places())

    def smart_computer_turn(self):  # Smart computer turn using the dictionary
        current_board = self.board.copy()
        empty = self.empty_places()
        best_move = random.choice(empty)
        best_score = -1
        for i in empty:  # Goes over all empty spots
            current_board[i] = 2
            key = ''.join(map(str, current_board))
            if key in self.dictionary and self.dictionary[key][0] >= best_score:  # Checks for the max score
                best_score = self.dictionary[key][0]
                best_move = i
            current_board = self.board.copy()
        self.turn += 1
        # print(best_move, best_score)
        return best_move  # Returns the best move position for the computer

    def model_predict(self):  # Smart computer turn using the neural network
        he_can_win = self.can_win(0)  # Checks if the player can win in any position
        you_can_win = self.can_win(2)  # Checks if the computer can win in any position
        if he_can_win != -1 and you_can_win == -1:  # If the player can win and the computer cannot, block the player
            self.turn += 1
            # print("block!")
            return he_can_win
        current_board = self.board.copy()
        empty = self.empty_places()
        best_move = random.choice(empty)
        best_score = -1
        for i in empty:  # Goes over all empty spots on the game board
            current_board[i] = 2
            winner = np.array(current_board).reshape(-1, 1).T
            result = self.model_j.predict(winner, verbose=0)
            if result >= best_score:  # Checks for the max score
                best_score = result
                best_move = i
            current_board = self.board.copy()
        self.turn += 1
        # print(best_move, best_score)
        return best_move  # Returns the best move position for the computer

    # ----------------------------------------------------------------------------

    def play_100000_games(self):  # Plays 100,000 games of computer vs random computer
        player1 = 0  # Count of times computer 1 won
        player2 = 0  # Count of times computer 2 won
        for i in range(10000):  # For 100,000 games
            score = self.play_one_game_computer()  # Plays one game of computer vs computer
            if score == 'lose':  # If computer 1 won
                player1 += 1  # Adds a win for computer 1
            if score == 'win':  # If computer 2 won
                player2 += 1  # Adds a win for computer 2
            print(player1, player2)  # Prints out wins for both computers

    def play_one_game_computer(self):  # Plays one game of computer vs computer
        self.init_board()  # Resets the game board
        score = 'not over'  # Initializes game status
        while score == 'not over':  # While game is not over
            self.board[self.computer_turn()] = 0  # Sets the position for computer 1
            score = self.check_win()  # Checks if anyone won
            if score == 'not over':  # If game is still not over
                self.board[self.computer_turn()] = 2  # Sets the position for computer 2
                score = self.check_win()  # Checks if anyone won
        return score  # Returns the result of the game

    def play_one_game_smart_computer(
            self):  # Plays one game between a random computer and a smart computer using a dictionary/neural network, returning the game result (win/lose/not over)
        self.init_board()  # Initializes the game board
        self.save_boards = []  # Initializes the list to save game boards
        who_won = 'not over'  # Tracks the result of the last game
        self.turn = 1  # Counts the number of turns played
        self.save_boards.append(self.board.copy())  # Adds the game board to the list of boards
        while who_won == 'not over' and self.turn <= 16:  # While there is no winner and the game has not exceeded 16 turns
            if self.turn % 2 == 0:  # If it's computer 0's turn
                self.board[self.computer_turn()] = 0  # Computer 0 plays
            else:  # If it's computer 2's turn
                self.board[self.smart_computer_turn()] = 2  # Computer 2 plays smartly using a dictionary
                # self.board[self.model_predict()] = 2 # Computer 2 plays smartly using a neural network
            self.save_boards.append(self.board.copy())  # Adds the game board to the list of boards
            who_won = self.check_win()  # Checks if someone has won
        self.order_dictionary()  # Reorders the dictionary based on game boards
        return who_won  # Returns the game result (win/lose/not over = tie)

    def play_100000_smart_games(self):  # Plays 100,000 games between a smart computer and a random computer
        player1 = 0  # Tracks the number of wins for computer 1
        player2 = 0  # Tracks the number of wins for computer 2
        for i in range(1000):  # For 100,000 games
            if i % 100000 == 0:
                print(i)
            score = self.play_one_game_smart_computer()  # Plays one game between computers
            if score == 'lose':  # If computer 1 won
                player1 += 1  # Adds a win to computer 1
            elif score == 'win':  # If computer 2 won
                player2 += 1  # Adds a win to computer 2

        print("Agent: ", (player1 / 1000) * 100, "%")  # Prints the win percentage of computer 1
        print("Random Computer: ", (player2 / 1000) * 100, "%")  # Prints the win percentage of computer 2

# ----------------------------------------------------------------------------
if __name__ == '__main__':
    game = Game()  # Creates the game instance

    start = time.time()  # Records the start time
    game.play_100000_smart_games()
    # game.createDataFile() # Creates the dictionary
    end = time.time() - start
    print(int(end // 60), ":", int(end % 60))  # Prints the time taken for the code to run
