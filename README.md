# QChess
A chess-variant, in which you only state to which square you move, and the game then is a superposition of all game-states in which this is possible, as soon as you make a move that is only possible in some of the states, the game collapses into only those states. The game ends once a player checkmates the opponent in one of the states or a player cannot move in any state.

Check and capture must be specified, Castling is possible. 

En-Passant is not included.
Example-moves are c3, xd5, c6 check, xa5 check, Castle King, Castle Queen.

En-Passant is not (yet) included.



An example for a starting-game:

White: c3 - 2 states

Black: c6 - 4 states

White: d5 - 2 states

Black: xd5 - 1 state

...


The code is a single .py-file

Work in progress
