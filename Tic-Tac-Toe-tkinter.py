import numpy as np
import tkinter as tk
import tkinter.messagebox as msg
import copy
# import tensorflow as tf


NO_ROWS = 3
NO_COLS = 3


class board():
    def __init__(self, n_rows=NO_ROWS, n_cols=NO_COLS, p1='Player 1', p2='Player 2'):
        self.grid = np.zeros(n_rows*n_cols).reshape(n_rows,n_cols)
        self.gameOver = False
        self.lastMoved = 0
        self.p1 = p1
        self.p2 = p2
        # self.model = tf.keras.models.load_model('./ttt-model/')

    def getPlayerName(self, playerID):
        if playerID==0:
            return 'no one'
        elif playerID==1:
            return self.p1
        elif playerID==-1:
            return self.p2

    def getPlayerID(self, playerName):
        if (playerName==self.p1) | (playerName=='1'):
            return 1
        elif (playerName==self.p2) | (playerName=='2'):
            return -1
    
    def checkGameOver(self):
        # Checking rows
        if 3 in np.sum(self.grid, axis=0):
            self.gameOver = True
            return 1
        elif -3 in np.sum(self.grid, axis=0):
            self.gameOver = True
            return -1
        # Checking columns
        elif 3 in np.sum(self.grid, axis=1):
            self.gameOver = True
            return 1
        elif -3 in np.sum(self.grid, axis=1):
            self.gameOver = True
            return -1
        # Checking diagonals
        d1 = np.sum(self.grid * np.eye(self.grid.shape[0]))
        d2 = np.sum(self.grid * np.fliplr(np.eye(self.grid.shape[0])))
        if (d1==3) | (d2==3):
            self.gameOver = True
            return 1
        elif (d1==-3) | (d2==-3):
            self.gameOver = True
            return -1
        
        if 0 not in self.grid:
            self.gameOver = True
            return 0
    
    def makeMove(self, playerName, pos):
        playerID = self.getPlayerID(str(playerName))
        if self.gameOver:
            return False
        if self.grid[pos] == 0:
            if not self.lastMoved == playerID:
                self.grid[pos] = playerID
                self.lastMoved = playerID
                # self.showBoard()
                winner = self.checkGameOver()
                # if self.gameOver:
                #     print(f"Game Over!! Winner is {self.getPlayerName(winner)}")
                    
            else:
                print('Same Player cannot play twice in a row!!!')
                return False
        else:
            print('Occupied Space!!!')
            return False
        return True

    def showBoard(self):
        boardState = '-------------------\n'
        for i in range(self.grid.shape[0]):
            # boardState = boardState+'|\t'
            for j in range(self.grid.shape[1]):
                if self.grid[i,j] == 0:
                    boardState = boardState+'|     '
                elif self.grid[i,j] == 1:
                    boardState = boardState+'|  +  '
                else:
                    boardState = boardState+'|  o  '
            boardState = boardState+'|\n'
            boardState = boardState+'-------------------\n'
        print(boardState)

    # def getBoardState(self):
    #     return self.grid.reshape(-1)

    # def selectOptimalPlay(self,playerName):
    #     pid = self.getPlayerID(str(playerName))
    #     currentState = self.getBoardState()
    #     empty_spots = np.where(currentState==0)[0]
    #     probable_winner = []
    #     for pos in empty_spots:
    #         tentativeState = currentState.copy()
    #         tentativeState[pos] = pid
    #         probable_winner.append(self.model.predict(np.array(tentativeState).reshape(1,9)))
    #     bestPlay = np.argmin(np.abs(([x-pid for x in probable_winner])))
    #     row = int(bestPlay/NO_COLS)
    #     col = int(bestPlay%NO_COLS)
    #     return (row,col)



# b1 = board(p1='A', p2='B')
# b1.makeMove(1,(0,0))
# b1.makeMove(2,(0,1))
# b1.makeMove(1,(1,1))
# b1.makeMove(2,(1,0))
# b1.makeMove(1,(1,2))
# b1.makeMove(2,(2,2))
# b1.makeMove(1,(2,0))
# b1.makeMove(2,(2,1))
# b1.makeMove(1,(0,2))

b1 = board()
currentPlayer = 1

def start_game():
    global b1, currentPlayer
    b1 = board()
    currentPlayer = 1
    canvas.delete('all')
    canvas.config(cursor='X_cursor')
    canvas.create_line(100,10,100,290,fill='white')
    canvas.create_line(200,10,200,290,fill='white')
    canvas.create_line(10,100,290,100,fill='white')
    canvas.create_line(10,200,290,200,fill='white')

def drawSymbol(row, col, player):
    cell_height = canvas.winfo_reqheight()/3
    cell_width = canvas.winfo_width()/3
    x1 = col*cell_width+20
    y1 = row*cell_height+20
    x2 = (col+1)*cell_width-20
    y2 = (row+1)*cell_height-20
    if player==2:
        canvas.create_oval(x1-5,y1-5,x2-5,y2-5,outline='white',width=5)
    else:
        canvas.create_line(x1,y1,x2,y2,fill='white',width=5)
        canvas.create_line(x1,y2,x2,y1,fill='white',width=5)

def makeMark(event):
    global b1, currentPlayer
    x,y = event.x,event.y
    (h,w) = (canvas.winfo_height(), canvas.winfo_width())
    row = int(NO_ROWS*y/h)
    col = int(NO_COLS*x/w)
    # b1.makeMove(currentPlayer, (row,col))
    if not b1.makeMove(currentPlayer, (row,col)):
        return
    if currentPlayer==1:
        drawSymbol(row,col,currentPlayer)
        currentPlayer = 2 
        canvas.config(cursor='circle')
    else:
    #     (row,col) = b1.selectOptimalPlay(currentPlayer)
    #     if not b1.makeMove(currentPlayer, (row,col)):
    #         return
        drawSymbol(row,col,currentPlayer)
        currentPlayer = 1 
        canvas.config(cursor='X_cursor')
    if isinstance(b1.checkGameOver(), int):
        message = f"Game Over!! Winner is {b1.getPlayerName(b1.checkGameOver())}"
        if msg.askretrycancel(title='Game Finished', message=message, parent=main_screen):
            start_game()





root = tk.Tk()
root.title('Tic-Tac-Toe')

main_screen = tk.Frame(root)
main_screen.grid(column=0, columnspan=5, row=0, rowspan=5, padx=5, pady=5)

# end_message = tk.Toplevel(root)
# restart_game_buttton = tk.Button(end_message, text='Restart Game', command=start_game)
# restart_game_buttton.grid(row=1, column=0)

canvas = tk.Canvas(main_screen, width=300, height=300, background='black', cursor='X_cursor')
canvas.create_line(100,10,100,290,fill='white')
canvas.create_line(200,10,200,290,fill='white')
canvas.create_line(10,100,290,100,fill='white')
canvas.create_line(10,200,290,200,fill='white')
canvas.bind('<Button-1>', func=makeMark)
canvas.pack()

side_menu = tk.Frame(root)
side_menu.grid(column=5, columnspan=1, row=0, rowspan=5, padx=5, pady=5)

reset_button = tk.Button(side_menu, text='Reset', command=start_game)
reset_button.pack()

root.mainloop()