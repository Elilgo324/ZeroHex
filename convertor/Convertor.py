# script gets HEX games in letters like: W[aa];B[bb];W[cd];B[dd])
# prints the board in every step
import numpy as np
path = "NEW1999CHANGED.txt"

def main():
    c = Convertor(path, 11)
    c.convert()

class Convertor:
    def __init__(self, path, board_size):
        self.path = path
        self.board_size = board_size

    def getNumeric(self, letter):
        return ord(letter) - 97

    def convert(self):
        class Turn:
            W = 0
            B = 1

        # open file of games. read one game
        f = open(path, "r")
        # initialize board with 0's
        Wboard = np.zeros((self.board_size, self.board_size))
        Bboard = np.zeros((self.board_size, self.board_size))
        board = [Wboard, Bboard]
        # save name of the player
        name = f.readline()
        print("Player Name: {}".format(name))
        for line in f.readlines():
            print(line)

            # organize locations
            sp_line = line.split(";")
            locations = []
            for loc in sp_line:
                x_val = self.getNumeric(loc[2])
                y_val = self.getNumeric(loc[3])
                location = [x_val, y_val]
                locations.append(location)
            print(locations)

            turn = Turn.W
            # modify board
            for locat in locations:
                print("its %s turn:" % turn)
                if locat[0] > self.board_size:  # ignore other letters
                    print("user {} left the game".format(turn))
                    continue
                board[turn][locat[0], locat[1]] = 1
                turn = (turn + 1) % 2
                print(board)

if __name__ == "__main__":
    main()

