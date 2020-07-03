# TicTacToe-Minimax

An AI for Tic Tac Toe created using the minimax algorithm. Player interacts with the game engine through a graphical interface. Alpha-beta pruning will be added to the algorithm to increase its efficiency by reducing the total number of required comparisons.

# Terminal Version

First I decided to get a terminal based version of the game running. The controls for the board were managed by assigning each square on the grid a value, which will be selected to place a player's token there. Having made the implementation scable, the size of the boad can be increased to any value alongside the num of players, although I have limited this to six at the momen, since there are only six hard coded player tokens. 

![basic board](imgs/noColourBoard.png) 

The basic printing of the board was in just black and white, which I frankly found too dull, so I added some colour formating to the board and the tokens.

![basic board](imgs/colouredBoard.png) 

I added a variety of colours for the player tokens and made the game randomly assign one to each player at the start of each game. Now it looks better! 

After adding Minimax I noticed that the first few moves take the longest to compute due to the shear amount of game states to explore. Adding alpha beta pruning improved this a lot with upwards of 93% deduction in the number of comparisons in some cases. 

![basic board](imgs/pruningImprovement.png) 

Despite this, for larger boards, even just for a 4x4, then intial couple of moves have comparisons in the magnitude of 10s of millions, so further optimisation is required. 
