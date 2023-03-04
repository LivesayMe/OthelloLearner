# RL Agent to Play Othello

To run alternate between calling simulate_games() in cli.py and the training.py file. You can play against it by calling play_nn() in cli.py or evaluate it against a random player with evalute_nn().

simulate_games() has the current agent loaded from model.h5 play n games against itself, where n is from the command line argument. The history of all of the games is stored in data.txt.

In training the input is the board state, and the output is the ratio of the number of times white has won over all games. 

Currently there is an issue where game states that are very different don't get learned very well, which results in the agent being very bad at end games. In games like blocks this is less of a problem since all states are equally likely to show up, not just the first few states.

Below is model architecture.

![model](https://user-images.githubusercontent.com/48233071/222905154-5acb8464-ac51-484f-b8e6-0bdb0a881a4b.png)

It has a total of 18,000 parameters.

See old implementation here https://github.com/LivesayMe/RL_Othello



I've implemented this algorithm into my puzzle website! It is trained to play the puzzle game Blocks. You can play it here https://np-problems.web.app/aiblocks
