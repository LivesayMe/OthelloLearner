# MCTS.py
# Author: Hunter Livesay
# Date: 1/6/2023
# Description: Implements the reinforcement MCTS algorithm for the Othello game
# General Notes
# Black = -1, White = 1, Empty = 0

# 1. Selection
#   1.1. Select the node with the highest UCT value
# 2. Expansion
#   2.1. If the node is terminal, return the node
#   2.2. If the node is not terminal, expand the node
# 3. Simulation
#   3.1. Play the game out randomly until the game is over
# 4. Backpropagation
#   4.1. Update the node with the result of the game

import random
from player import NN_Player
import othello
import math


#Load model
player = NN_Player()

def get_value(node):
    if node.is_terminal:
        return node.state.get_winner()
    else:
        return player.get_value(node.state) / 4

class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.wins = 0
        self.visits = 0
        self.losses = 0
        self.ties = 0
        self.is_terminal = False

    def add_child(self, child):
        self.children.append(child)

    def update(self, result):
        self.visits += 1
        if result == 1:
            self.wins += 1
        elif result == -1:
            self.losses += 1
        else:
            self.ties += 1
    
    def expansion(self):
        moves, count = self.state.get_possible_moves(self.state.cur_player)
        for i in range(count):
            child = Node(self.state.copy(), self)
            child.state.make_move(child.state.cur_player, [moves[i][0], moves[i][1]])
            child.is_terminal = child.state.is_game_over()
            self.add_child(child)
        print(count)
        return self.children[random.randint(0, len(self.children) - 1)]
    
    def get_best_child(self):
        best_value = -math.inf
        best_child = None
        for child in self.children:
            v = 1
            if child.visits > 0:
                v = math.log(self.visits) / child.visits
            value = get_value(child) + math.sqrt(2 * v)
            if value > best_value:
                best_value = value
                best_child = child
        return best_child

    def selection(self):
        if self.is_terminal:
            return None
        if len(self.children) == 0:
            return self.expansion()
        else:
            return self.get_best_child().selection()

    def rollout(self):
        game = self.state.copy()
        while not game.is_game_over():
            move, score, prediction = player.get_move(game)
            game.make_move(game.cur_player, [move[0], move[1]])
        self.backpropagate(game.get_winner())
        return game
    
    def backpropagate(self, result):
        self.update(result)
        if self.parent:
            self.parent.backpropagate(result)
    
    def write_node(self, f):
        f.write(
            self.state.get_fen() + "#" + str(1.0 * self.wins / self.visits) + " " + str(1.0 * self.losses / self.visits) + " " + str(1.0 * self.ties / self.visits) + "\n"
        )
        for child in self.children:
            if child.visits > 0:
                child.write_node(f)
    

def MCTS(root, iterations):
    for i in range(iterations):
        node = root.selection()
        if node is None:
            node = root
        print("Exploring state")
        node.state.print_board()
        print("Visited: %s Won:%s" % (node.visits, node.wins))
        node.rollout()

    f = open("MCTS.txt", "w+")
    root.write_node(f)
    f.close()

root = Node(othello.Othello())
MCTS(root, 600)
    

