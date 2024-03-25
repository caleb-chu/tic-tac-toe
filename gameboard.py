import tkinter as tk

class BoardClass:
    def __init__(self, my_player1_name: str, my_player2_name:str):
        """
        Initializes a BoardClass instance.

        Args:
        - my_player_name (str, optional): The username of the player (default: '').

        Example usage:
        board = BoardClass(player1_username)
        """

        self.player1user = my_player1_name
        self.player2user = my_player2_name
        self.last_player = None
        self.num_wins = 0
        self.num_ties = 0
        self.num_losses = 0
        self.num_games = 0

    def updateGamesPlayed(self):
        """
        Updates the number of games played by the player.

        Example usage:
        board.updateGamesPlayed()
        """
        self.num_games += 1

    def resetGameBoard(self):
        """
        Resets the game board to the default state (3 rows of 3 spaces).

        Example usage:
        board.resetGameBoard()
        """
        self.game_board = [[" "," "," "], [" "," "," "], [" "," "," "]]

    def printGameBoard(self):
        """
        Prints the game board.

        Example usage:
        board.printGameBoard()
        """
        for i in self.game_board:
            print(i)
        print()

    def updateGameBoard(self, player, symbol, row, col):
        """
        Updates the game board with a player's move.

        Args:
        - player (str): The username of the player making the move.
        - symbol (str): The symbol representing the player's move ('x' or 'o').
        - row (int): The row coordinate of the move (0, 1, or 2).
        - col (int): The column coordinate of the move (0, 1, or 2).

        Returns:
        bool: True if the game board is updated, False otherwise.

        Example usage:
        board.updateGameBoard(player1_username, "x", 0, 0)
        """
        if self.game_board[row][col] == " ":
            self.game_board[row][col] = symbol
            self.last_player = player 
            return True
        else:
            return False

    def isWinner(self):
        """
        Checks if there is a winner on the game board.

        Returns:
        bool: True if there is a winner, False otherwise.

        Example usage:
        if board.isWinner():
            print("We have a winner!")
        """
        for row in self.game_board:
            if row[0] == row[1] == row[2]  and row[0] != ' ':
                return True
        
        for i in range(3):
            if self.game_board[0][i] == self.game_board[1][i] == self.game_board[2][i] != " ":
                return True
        
        if self.game_board[0][0] == self.game_board[1][1] == self.game_board[2][2]  != " ":
            return True
        
        if self.game_board[0][2] == self.game_board[1][1] == self.game_board[2][0] != " ":
            return True
        
        return False

    def didIWin(self, letter):
        """
        Checks if the player with the specified symbol has won the game.

        Args:
        - letter (str): The symbol representing the player's move ('x' or 'o').

        Returns:
        bool: True if the player has won, False otherwise.

        Example usage:
        if board.didIWin("x"):
            print("Congratulations! You won!")
        """
        for row in self.game_board:
            if row[0] == row[1] == row[2] == letter and row[0] != ' ':
                return True
        
        for i in range(3):
            if self.game_board[0][i] == self.game_board[1][i] == self.game_board[2][i] == letter != " ":
                return True
        
        if self.game_board[0][0] == self.game_board[1][1] == self.game_board[2][2] == letter != " ":
            return True
        
        if self.game_board[0][2] == self.game_board[1][1] == self.game_board[2][0] == letter != " ":
            return True
        
        return False

    def boardIsFull(self):
        """
        Checks if the game board is full (no empty spaces).

        Returns:
        bool: True if the board is full, False otherwise.

        Example usage:
        if board.boardIsFull():
            print("It's a tie! The board is full.")
        """
        for row in self.game_board:
            for col in row:
                if col == " ":
                    return False
        self.num_ties += 1
        return True

    def updateWinCount(self):
        """
        Updates the win count when the player wins the game.

        Example usage:
        board.updateWinCount()
        """
        self.num_wins += 1

    def updateLossCount(self):
        """
        Updates the loss count when the player loses the game.

        Example usage:
        board.updateLossCount()
        """
        self.num_losses += 1

    def printStats(self):
        """
        Prints the player's game statistics.

        Example usage:
        board.printStats()
        """
        print(f"Player1 username: {self.player1user}")
        print(f"Player2 username: {self.player2user}")
        print(f"Last player: {self.last_player}")
        print(f"Number of Wins: {self.num_wins}")
        print(f"Number of Ties: {self.num_ties}")
        print(f"Number of Losses: {self.num_losses}")
        print(f"Number of Games: {self.num_games}")
