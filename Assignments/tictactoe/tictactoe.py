"""
Tic Tac Toe Player
"""

import math
import copy
from queue import PriorityQueue # Originally was going to use a priority queue to automatically order moves
# However ended up with AI making irrational moves so just switched to returning a single good move

X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board.
    """
    # return [[O, X, X],
    #          [X, O, O],
    #          [O, O, EMPTY]]
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    noughts = 0
    crosses = 0

    for row in board:
        for tile in row:
            if tile == O: noughts += 1
            elif tile == X: crosses += 1
    
    if noughts < crosses: return O
    if noughts > crosses: return X
    
    return X # If entire board is empty return X since X always starts first

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] is EMPTY: moves.add((i, j))

    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    clone = copy.deepcopy(board)
    row = action[0]
    column = action[1]

    if clone[row][column] is EMPTY:
        clone[row][column] = player(clone)
        return clone
    
    raise RuntimeError

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # Search rows
    for row in board:
        noughts = 0
        crosses = 0

        for tile in row:
            if tile == X: crosses += 1
            elif tile == O: noughts += 1

        if crosses == 3: return X
        if noughts == 3: return O

    # Search columns
    for i in range(3):
        noughts = 0
        crosses = 0

        for j in range(3):
            if board[j][i] == X: crosses += 1
            elif board[j][i] == O: noughts += 1

        if crosses == 3: return X
        if noughts == 3: return O
    
    # Search diagonals
    noughts = 0
    crosses = 0
    j = 0
    for i in range(3):
        if board[i][j] == X: crosses += 1
        elif board[i][j] == O: noughts += 1
        j += 1
    
    if crosses == 3: return X
    if noughts == 3: return O

    noughts = 0
    crosses = 0
    j = 2
    for i in range(3):
        if board[i][j] == X: crosses += 1
        elif board[i][j] == O: noughts += 1
        j -= 1
    
    if crosses == 3: return X
    if noughts == 3: return O

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # if winner or there are no more possible actions
    if winner(board) is not None or actions(board) == set(): return True
    return False

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X: return 1
    if winner(board) == O: return -1

    return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    # If the player is X it will try to maximise the 

    if terminal(board): return None
    
    current = player(board)
    bestAction = None

    if current == X:
        bestAction = maximise(board, -float("inf"), float("inf"))[1]
    elif current == O:
        bestAction = minimise(board, -float("inf"), float("inf"))[1]
    
    if bestAction is None: raise RuntimeError

    return bestAction

# Note to self: alpha represents the best score the maximiser can achieve at that layer in the tree or above
# Beta represents the best score the minimiser can achieve at that layer in the tree or above

def maximise(board, alpha, beta): 
    """
    Returns the best score for an agent attempting to maximise its score
    """
    if terminal(board): return (utility(board), None)
    val = -float("inf")
    bestAction = None

    for action in actions(board):
        minimisedVal = minimise(result(board, action), alpha, beta)[0] # Best value opponent can select
        if val < minimisedVal:
            val = minimisedVal
            bestAction = action

            alpha = max(alpha, minimisedVal)
            if beta <= alpha: # If the best score the minimiser has cannot beat the maximiser
                break

    return (val, bestAction)

def minimise(board, alpha, beta):
    """
    Returns the best score for an agent attempting to minimise its score
    """
    if terminal(board): return (utility(board), None)
    val = float("inf")
    bestAction = None

    for action in actions(board):
        maximisedVal = maximise(result(board, action), alpha, beta)[0] # Best value opponent can select
        if val > maximisedVal:
            val = maximisedVal
            bestAction = action

            beta = min(beta, maximisedVal)
            if beta <= alpha:
                break

    return (val, bestAction)