import tkinter as tk
import socket
from threading import *
from gameboard import BoardClass

class player1():
    master = 0
    player2_hostName = 0
    port_number = 0
    player1_username = 0
    try_again = 0
    buttons = []
    move_label = 0
    
    def __init__(self) -> None:
        self.createConnectionPopup()

    def createConnectionPopup(self) -> None:
        self.master = tk.Tk()
        self.master.title("Player 1: Connect to player 2") #sets the window title
        self.master.geometry('400x400') #sets the default size of the window
        self.master.resizable(0,0) #setting the x(horizontal) and y (verticl) to not be resizable

        self.player2_hostName = tk.StringVar()
        self.port_number = tk.IntVar()
        self.player1_username = tk.StringVar()
        self.try_again = tk.StringVar()

        self.ip_label = tk.Label(self.master, text = "Enter player2's host name:")
        self.ip_entry = tk.Entry(self.master, textvariable = self.player2_hostName)
        self.ip_label.pack()
        self.ip_entry.pack()

        self.port_label = tk.Label(self.master, text = "Enter player2's host number:")
        self.port_entry = tk.Entry(self.master, textvariable = self.port_number)
        self.port_label.pack()
        self.port_entry.pack()

        self.submit_button = tk.Button(self.master, text = "Enter", command=self.establish_connection)
        self.submit_button.pack()
    
    def establish_connection(self)->None:
        self.connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.connection_socket.connect((self.player2_hostName.get(), self.port_number.get()))
            self.create_username_entry()
        except:
            self.try_connection_again()

    def create_username_entry(self)->None:
        self.accepted_connection_label = tk.Label(self.master, text = "Connection was successful")
        self.username_label = tk.Label(self.master, text = "Enter your alphanumberic username:")
        self.username_entry = tk.Entry(self.master, textvariable = self.player1_username)
        self.accepted_connection_label.pack()
        self.username_label.pack()
        self.username_entry.pack()
        self.username_submit_button = tk.Button(self.master, text = "Enter", command=self.check_username)
        self.username_submit_button.pack()
    
    def username_error_message(self) -> None:
        self.error_username_label = tk.Label(self.master, text = "Username must have numbers and letters in order to connect, try again.")
        self.error_username_label.pack()

    def send_receive_username(self) -> None:
        #Send the username to player 2
        self.connection_socket.send(self.player1_username.get().encode())
        #Receive player2's username
        self.player2_username = self.connection_socket.recv(1024).decode()
        self.run_game()
        self.make_board()

    def check_username(self) -> None:
        if self.player1_username.get().isalnum() == False:
            self.username_error_message()
            self.create_username_entry()
        else:
            self.send_receive_username()

    def try_connection_again(self)->None:
        self.try_again_label = tk.Label(self.master, text = "There was an issue connecting to the server. Would you like to try again? (y/n):")
        self.try_again_Entry = tk.Entry(self.master, textvariable = self.try_again)
        self.try_again_label.pack()
        self.try_again_Entry.pack()
        self.try_again_submit_button = tk.Button(self.master, text = "Enter", command=self.check_try_again)
        self.try_again_submit_button.pack()

    def check_try_again(self) -> None:
        if self.try_again.get().lower() == 'y':
            self.master.destroy()
            player1()
        else:
            self.master.destroy()
    
    def run_game(self) -> None:
        self.myGame = BoardClass(self.player1_username.get(), self.player2_username)
        self.myGame.updateGamesPlayed()

        self.master.destroy()
        self.master = tk.Tk()
        self.master.title(f"{self.player1_username.get()}'s board")
        self.master.geometry('500x500')
        self.master.resizable(0,0)
        self.movelabel = tk.Label(self.master, text = "Your turn")
        self.movelabel.grid(row=8, column=1)

    def make_board(self) -> None:
        self.master.update()
        if self.myGame.getGamesPlayed == 1:
            for row in range(3):
                row_buttons = []
                for col in range(3):
                    button = tk.Button(self.master, text='-', width=6, height=3, command=lambda r=row, c=col: self.myturn(r, c))
                    button.grid(row=row, column=col, padx=5, pady=5)
                    row_buttons.append(button)
                self.buttons.append(row_buttons)
        self.movelabel.configure(text = "Your turn.")

    def my_turn(self, row: int, col: int) -> None:
        self.master.update()
        button = self.buttons[row][col]
        self.myGame.updateGameBoard(self.player1_username, "X", row, col)
        button.config(text="X", state="disabled")
        self.master.update()
        self.connection_socket.send(str(row * 10 + col).encode())


    def runUI(self) -> None:
        self.master.mainloop()

"""
def createConnectionPopup(player2_socket:socket):
    username, player2_username = "", ""

    def connect_to_player2():
        player2_host = label2.get()  # Get the value from label2
        player2_port = label4.get()
        try:
            #player2_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            player2_socket.connect((player2_host, int(player2_port)))
            goodlabel = tk.Label(root, text='Connection accepted')
            goodlabel.pack()
            buildUserBlocks()
            # Perform further operations with the connection to player 1
        except ConnectionRefusedError:
            print("Connection refused. Player 2 is not available.")
            badlabel = tk.Label(root, text='Connection refused')
            badlabel.pack()

    def buildUserBlocks():
        def sendUsername():
            nonlocal username, player2_username

            username = usernameEntry.get()
            encoded = username.encode()
            player2_socket.sendall(encoded)
            sent = tk.Label(root, text='Your username has been sent')
            sent.pack()
            player2_username = player2_socket.recv(1024).decode()
            root.destroy()

        usernamelabel = tk.Label(root, text='Enter your username:')
        usernamelabel.pack()

        usernameEntry = tk.Entry(root)
        usernameEntry.pack()

        sendUser = tk.Button(root, text="Send Username", command=sendUsername)
        sendUser.pack()

    root = tk.Tk()
    root.title('Try to connect to player 2')
    root.geometry("400x250")

    label1 = tk.Label(root, text='Player 2 Host:')
    label1.pack()

    label2 = tk.Entry(root)
    label2.pack()

    label3 = tk.Label(root, text='Player 2 Port:')
    label3.pack()

    label4 = tk.Entry(root)
    label4.pack()

    makeConnection = tk.Button(root, text="Connect to player 2", command=connect_to_player2)
    makeConnection.pack()

    root.mainloop()
    return username, player2_username

"""

"""
def handle_button_click(button,board:BoardClass, row:int, col:int, player, otherPlayer, mysocket:socket, myTk:tk):
    button.config(text="x")  # Update the button's text to display 'x'
    button.config(state="disabled")
    board.updateGameBoard(player, "x", row, col)
    rowcol = str(row) + str(col)
    mysocket.send(rowcol.encode()) #problem line
    label3 = tk.Label(myTk, text='Your move has been sent:')
    label3.pack()

def runGame(user, user2, board:BoardClass, mysocket:socket):
    board.resetGameBoard()
    root = tk.Tk()
    root.title(f"{user}'s game with {user2}")
    root.geometry("400x400")
    #mysocket.sendall(user.encode())
    for row in range(3):
        for col in range(3):
            button = tk.Button(root, text="", width=5, height=4)
            button.grid(row=row, column=col, padx=10, pady=10)
            button.config(command=lambda btn=button: handle_button_click(btn,board,row,col, user, user2, mysocket, root))
    root.mainloop() 
"""

if __name__ == "__main__":

    """mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    user1, user2 = createConnectionPopup(mysocket)
    board = BoardClass(user1, user2)
    runGame(user1, user2, board, mysocket)
    print('Hello World')"""

    player1_game = player1()
