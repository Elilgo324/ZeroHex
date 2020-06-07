import numpy
import sys
import random


def flip_move(move):
    return move[1], move[0]


def new_board(size):
    return numpy.zeros((2, size, size))


def make_move(board, move):
    '''
    Mutably make a move, flipping the board so that vertical is still the next
    player to move.
    '''
    board[0,move[0],move[1]] = 1
    return flip(board)


def flip(board):
    '''
    Swaps vertical and horizontal players.
    '''
    return numpy.flip(numpy.transpose(board, (0, 2, 1)), 0)


def symmetry(board):
    '''
    Apply the symmetry of the board (flipping both axes).
    '''
    return numpy.flip(numpy.flip(board, 1), 2)


def symmetry_probs(probs):
    return numpy.flip(numpy.flip(probs, 0), 1)


def dfs(board, x, y, visited):
    size = board.shape[1]
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx == 0 and dy == 0 or dx * dy == 1:
                continue
            nx, ny = x + dx, y + dy
            if nx < 0 or nx >= size or ny < 0 or ny >= size:
                continue
            if board[1,nx,ny] == 0:
                continue
            if nx == size - 1:
                return True
            if (nx, ny) in visited:
                continue
            visited.add((nx, ny))
            if dfs(board, nx, ny, visited):
                return True
    return False


def winner(board):
    '''
    Calculates whether the second/horizontal player has won the game. Note that
    since we always rotate the board so that the player to move is the vertical
    player, we do not need to check whether the vertical player has won.
    '''
    size = board.shape[1]
    visited = set()
    for y in range(size):
        if board[1,0,y] == 0:
            continue
        if (0, y) in visited:
            continue
        visited.add((0, y))
        if dfs(board, 0, y, visited):
            return True
    return False


def print_board(board, move=(-1, -1), file=sys.stdout):
    size = board.shape[1]
    for y in range(size):
        file.write(y * " ")
        for x in range(size):
            if x == move[0] and y == move[1]:
                if board[0,x,y] != 0:
                    s = "#"
                else:
                    s = "@"
            elif board[0,x,y] != 0:
                s = "X"
            elif board[1,x,y] != 0:
                s = "O"
            else:
                s = "."
            file.write((s + " ") if x < size - 1 else s)
        file.write("\n")


def normalize(probabilities):
    return numpy.copy(probabilities) / numpy.sum(probabilities, (0, 1))


def fix_probabilities(board, probabilities):
    '''
    Sets probabilities of illegal moves to zero.

    The raw output of the network gives a probability for every space on the
    board, which is not necessarily zero even if it already contain a stone. We
    need to fix this before sampling from the probability distribution to
    select a move.
    '''
    size = board.shape[1]
    result = numpy.copy(probabilities)
    for x in range(size):
        for y in range(size):
            if board[0,x,y] != 0 or board[1,x,y] != 0:
                result[x,y] = 0
    return normalize(result)


def best_move(probabilities):
    '''
    Selects the move with the highest probability. If tied, selects randomly.
    '''
    size = probabilities.shape[0]
    max_probability = max(probabilities[x,y] for x in range(size) for y in range(size))
    return random.choice(list((x, y) for x in range(size) for y in range(size) if probabilities[x,y] == max_probability))


def best_k_moves(probabilities, k):
    '''
    Selects the move with the highest probability. If tied, selects randomly.
    '''
    size = probabilities.shape[0]
    sorted_p = sorted([probabilities[x,y] for x in range(size) for y in range(size)], reverse=True)[:k]
    # max_probability = max(probabilities[x,y] for x in range(size) for y in range(size))
    return list((x, y) for x in range(size) for y in range(size) if probabilities[x,y] in sorted_p)

def top_11(probabilities):
    tops = []
    tops = numpy.argpartition(probabilities,-11)[-11:]
    print(tops)
    return tops


class Pos(object):
    def __init__(self, x, y) -> None:
        super().__init__()
        self.x = x
        self.y = y

    def __repr__(self):
        return '({}, {})'.format(self.x, self.y)


def refined_move(probabilities):
    size = probabilities.shape[0]
    board = [Pos(x, y) for x in range(size) for y in range(size)]
    probabilities = probabilities.reshape(size**2)
    pos = numpy.random.choice(board, p=probabilities)
    return pos.x, pos.y


def refined_moves(probabilities, set_len):
    # if random chose same index - probably we not need 15 results
    moves = set()
    size = probabilities.shape[0]
    board = [Pos(x, y) for x in range(size) for y in range(size)]
    probabilities = probabilities.reshape(size**2)
    while moves.__len__() < set_len:
        pos = numpy.random.choice(board, p=probabilities)
        moves.add(tuple([pos.x, pos.y]))
    return moves


def sample_move(probabilities):
    """
    Sample move from probability distribution.
    :param probabilities:
    :return:
    """
    size = probabilities.shape[0]
    r = random.random()
    for x in range(size):
        for y in range(size):
            prob = probabilities[x,y]
            if r < prob:
                return x, y
            r -= prob
    raise Exception('Failed to select move from probability distribution')


def write_move(move):
    return chr(ord('a') + move[0]) + str(move[1] + 1)


def read_move(move):
    return ord(move[0]) - ord('a'), int(move[1:]) - 1

