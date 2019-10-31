from random import choice
from sys import stdin


class HumanPlayer:
    """
    human player uses cmd
    """
    def __init__(self):
        self.name = "Human"

    def getMove(self,game):
        move = None
        while move not in game.availableMoves:
            print("select a row and column")
            try:
                line = stdin.readline().split()
                move = (int(line[0]),int(line[1]))
            except ValueError:
                print("invalid move")
            if move not in game.availableMoves:
                print("invalid move")
        return move


class RandomPlayer:
    """
    player that chooses random legal moves
    """
    def __init__(self):
        self.name = "Random"

    def getMove(self,game):
        # choice returns random move
        return choice(game.availableMoves)
