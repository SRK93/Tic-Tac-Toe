import numpy as np
import tensorflow as tf
import copy
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

NO_ROWS = 3
NO_COLS = 3


class board():
    def __init__(self, n_rows=NO_ROWS, n_cols=NO_COLS, p1='Player 1', p2='Player 2'):
        self.grid = np.zeros(n_rows*n_cols).reshape(n_rows,n_cols)
        self.gameOver = False
        self.lastMoved = 0
        self.p1 = p1
        self.p2 = p2

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

    def getBoardState(self):
        return self.grid.reshape(-1)


'''
Training the model
'''
# model = tf.keras.Sequential()

# model.add(tf.keras.layers.Dense(9,'relu'))
# model.add(tf.keras.layers.Dense(18,'relu'))
# model.add(tf.keras.layers.Dense(9,'relu'))
# model.add(tf.keras.layers.Dense(4,'relu'))
# model.add(tf.keras.layers.Dense(1,'tanh'))

# model.compile(optimizer='Adam', loss='mse')

# X =  np.empty((0,9), int)
# y =  np.empty((0,1), int)
# for i in range(10000):
#     b1 = board()
#     currentplayer=1
#     while not b1.gameOver:
#         empty_places = np.where(b1.getBoardState()==0)[0]
#         position = np.random.choice(empty_places)
#         row = int(position/NO_COLS)
#         col = int(position%NO_COLS)
#         b1.makeMove(currentplayer, (row,col))
#         if currentplayer==1:
#             currentplayer=2
#         else:
#             currentplayer=1
#     X = np.vstack([X,b1.getBoardState()])
#     y = np.vstack([y,b1.checkGameOver()])


# X_train,X_test,y_train,y_test = train_test_split(X,y,random_state=42)

# history = model.fit(x=X_train,y=y_train,epochs=10,validation_data=(X_test,y_test))

# model.save('./ttt-model/')


# plt.plot(history.history['loss'],label='Loss')
# plt.plot(history.history['val_loss'],label='Val_loss')
# plt.legend()
# plt.show()

'''
Using the trained model
'''

# model = tf.keras.models.load_model('./ttt-model/')

# test = np.array([-1,1,0,-1,0,1,1,0,0]).reshape(1,9)
# result = model.predict(test)
# print(result)

b1 = board()
b1.makeMove(1,(0,0))
