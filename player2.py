import tkinter as tk
from socket import *
from threading import *
from gameboard import BoardClass 



def createConnectionPopup(player1_socket:socket):
    clientSocket = None
    username, player1_username = "", ""
    def connectToPlayer1():
        def sendUsername():
            username = usernameEntry.get()
            encoded = username.encode()
            clientSocket.sendall(encoded)
            sent = tk.Label(root, text='Your username has been sent')
            sent.pack()
            root.destroy()
        player1_host = label2.get()  # Get the value from label2
        player1_port = label4.get()
        player1_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR,1)
        player1_socket.bind((player1_host, int(player1_port)))
        player1_socket.listen(1)
        clientSocket, clientAddress = player1_socket.accept()
        player1_username = clientSocket.recv(1024).decode()
        usernamelabel = tk.Label(root, text='Enter your username:')
        usernamelabel.pack()

        usernameEntry = tk.Entry(root)
        usernameEntry.pack()

        makeConnection = tk.Button(root, text="Connect to player 2", command=sendUsername)
        makeConnection.pack()

    root = tk.Tk()
    root.title('Try to connect to player 1')
    root.geometry("400x250")

    label1 = tk.Label(root, text='Player 1 Host:')
    label1.pack()

    label2 = tk.Entry(root)
    label2.pack()

    label3 = tk.Label(root, text='Player 1 Port:')
    label3.pack()

    label4 = tk.Entry(root)
    label4.pack()

    makeConnection = tk.Button(root, text = "Connect to player 1",command=connectToPlayer1)
    makeConnection.pack()

    root.mainloop()
    return player1_username, username

def runGame(user1, user2, mysocket:socket):
    root = tk.Tk()
    root.title("Player2's Game")
    root.geometry("400x400")
    #how to receive row and col
    #received_row_bytes = player1_socket.recv(1024).decode()  # Assuming 4-byte representation
    for row in range(3):
        for col in range(3):
            button = tk.Button(root, text="", width=5, height=4)
            button.grid(row=row, column=col, padx=10, pady=10)
            button.config(command=lambda btn=button: handle_button_click(btn))
    root.mainloop()

def handle_button_click(button):
    button.config(text="o")  # Update the button's text to display 'x'
    button.config(state="disabled")

if __name__ == "__main__":
    clientSocket = None
    player1_socket = socket(AF_INET, SOCK_STREAM)
    user1, user2 = createConnectionPopup(player1_socket)
    runGame(user1, user2, clientSocket)