import sys
sys.path.append('../game/')

from othello import Othello
from random import random, choice, randint
import player
import time

class Node:
    def __init__(self, state, is_terminal):
        self.state = state
        self.children = []
        self.visits = 0
        self.wins = 0
        self.losses = 0
        self.ties = 0
        self.move = None
        self.is_terminal = is_terminal
    
    def add_child(self, child):
        self.children.append(child)
    
    def get_child(self, move):
        for child in self.children:
            if child.move == move:
                return child
        return None

def play_random_game():
    game = Othello()
    while not game.is_game_over():
        moves, count = game.get_possible_moves(game.cur_player)
        move = moves[int(random() * count)]
        game.make_move(game.cur_player, [move[0], move[1]])
    return game

def play_against_ai():
    game = Othello()
    game.print_board()
    while not game.is_game_over():
        game.print_board()
        moves = game.get_possible_moves(game.cur_player)
        if game.cur_player == 1:
            print("White's turn")
            #Random move
            move = choice(moves)
            print("Move: ", move)
            game.make_move(game.cur_player, move)
        else:
            print("Black's turn")
            #Player move
            #Print valid moves with index
            for i in range(len(moves)):
                print(i, moves[i])
            move = input("Move: ")
            move = moves[int(move)]
            game.make_move(game.cur_player, move)
    print("Game Over")
    print("Winner: ", game.get_winner())

def explore_node(node):
    #If the node is terminal, return the winner
    if node.is_terminal:
        node.visits += 1
        result = node.state.get_winner()
        if result == 1:
            node.wins += 1
        elif result == -1:
            node.losses += 1
        else:
            node.ties += 1
        return result
    
    #If the node has no children, create children
    if len(node.children) == 0:
        moves, count = node.state.get_possible_moves(node.state.cur_player)
        for i in range(count):
            #Create a new game state
            new_state = node.state.copy()
            new_state.make_move(node.state.cur_player, [moves[i][0], moves[i][1]])
            #Create a new node
            new_node = Node(new_state, new_state.is_game_over())
            new_node.move = moves[i]
            #Add the node to the children
            node.add_child(new_node)
    
    #Select a child to explore
    child = choice(node.children)
    #Explore the child
    result = explore_node(child)
    #Update the node
    node.visits += 1
    if result == 1:
        node.wins += 1
    elif result == -1:
        node.losses += 1
    else:
        node.ties += 1
    return result

def write_node(node, f):
    #Write the node to a file
    f.write(node.state.get_fen())
    f.write("#")
    f.write(str(1.0 * node.wins / node.visits) + " " + str(1.0 * node.losses / node.visits) + " " + str(1.0 * node.ties / node.visits) + "\n")
    for child in node.children:
        if(child.visits > 0):
            write_node(child, f)

def simulate_games():
    #Play n games, and store fens along with the winner to a file
    #This will be used to train the neural network
    #Get n from command line
    n = int(sys.argv[1])
    
    root = Node(Othello(), False)
    for i in range(n):
        explore_node(root)
        print("Game: ", i, " Visits: ", root.visits, " Wins: ", root.wins)
    
    #Save every fen to a file
    f = open("data.txt", "w")
    write_node(root, f)
    f.close()    

def play_nn():
    nnPlayer = player.NN_Player()
    game = Othello()
    game.print_board()
    while not game.is_game_over():
        
        moves, count = game.get_possible_moves(game.cur_player)
        if game.cur_player == 1:
            print("White's turn")
            #nn move
            move, score, prediction = nnPlayer.get_move(game)
            print("Move: ", [move[0], move[1]], " Score: ", score, " Prediction: ", prediction)
            game.make_move(game.cur_player, [move[0], move[1]])
        else:
            print("Black's turn")
            #Player move
            #Print valid moves with index
            for i in range(count):
                print(i, [moves[i][0], moves[i][1]])
            move = input("Move: ")
            move = moves[int(move)]
            print(move)
            game.make_move(game.cur_player, [move[0], move[1]])
            print("Finished player turn")
        game.print_board()

    print("Winner: ", game.get_winner())

def evaluate_nn():
    #Play 10 games between nn and random
    #Print the results
    nnPlayer = player.NN_Player()
    nn_wins = 0
    random_wins = 0
    for i in range(10):
        game = Othello()
        while not game.is_game_over():
            
            if game.cur_player == 1:
                #nn move
                move, score, prediction = nnPlayer.get_move(game)
                game.make_move(game.cur_player, [move[0], move[1]])
            else:
                #Random move
                moves, count = game.get_possible_moves(game.cur_player)
                move = moves[randint(0, count - 1)]
                game.make_move(game.cur_player, [move[0], move[1]])
        winner = game.get_winner()
        if winner == 1:
            nn_wins += 1
        else:
            random_wins += 1
    print("NN Wins: ", nn_wins, " Random Wins: ", random_wins)

def main():    
    # play_nn()
    # simulate_games()
    evaluate_nn()

if __name__ == "__main__":
    main()
