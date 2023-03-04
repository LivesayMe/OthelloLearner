import sys
sys.path.append('../game/')

from othello import Othello
from random import random, choice
import time

import numpy as np
import tensorflow as tf
from tensorflow import keras
# import keras
from keras.layers import Dense, Conv2DTranspose, LeakyReLU, Reshape, BatchNormalization, Activation, Conv2D, Flatten, Dropout, Conv1D, Conv1DTranspose
from keras.models import Model, Sequential

class NN_Player():
    def __init__(self):
        self.model = tf.keras.models.load_model("saved_model/my_model")

    def get_value(self, game):
        #First convert game to a 65x1 numpy array
        board = game.board
        
        np_board = np.zeros((65,))
        for x in range(8):
            for y in range(8):
                np_board[x*8+y] = board[x][y]


        np_board[64] = game.cur_player
        np_board = np.reshape(np_board, (1, 65, 1))
        #Then pass it to the model
        prediction = self.model.predict(np_board, verbose=0)
        #Apply heuristic to the prediction (wins * 3 + ties * 1)
        if game.cur_player == 1:
            score = prediction[0][0] * 3 + prediction[0][2]
        else:
            score = prediction[0][1] * 3 + prediction[0][2]
        
        return score
    
    def get_move(self, game):
        
        best_score = -1
        best_move = None
        predict = []
        moves, count = game.get_possible_moves(game.cur_player)
        boards = []
        for i in range(count):
            cp = game.copy()
            cp.make_move(game.cur_player, [moves[i][0], moves[i][1]])
            #First convert game to a 65x1 numpy array
            board = cp.board
            
            np_board = np.zeros((65,))
            for x in range(8):
                for y in range(8):
                    np_board[x*8+y] = board[x][y]


            np_board[64] = game.cur_player
            boards.append(np_board)
        
        boards = np.array(boards)
        boards = np.reshape(boards, (count, 65, 1))
        #Then pass it to the model
        prediction = self.model.predict(boards, verbose=0)
        #Apply heuristic to the prediction (wins * 3 + ties * 1)
        for i in range(count):
            if game.cur_player == 1:
                score = prediction[i][0] * 3 + prediction[i][2]
            else:
                score = prediction[i][1] * 3 + prediction[i][2]
            # print("Move: ", [moves[i][0], moves[i][1]], "Score: ", score)
            if score > best_score:
                best_score = score
                best_move = moves[i]
                predict = prediction
        return best_move, best_score, predict



