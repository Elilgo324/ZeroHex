# script gets HEX games in letters like: W[aa];B[bb];W[cd];B[dd])
# prints the board in every step
import numpy as np
filename = "1563.txt"

def main():
    c = Convertor(filename, 11)
    c.convert()

class Convertor:
    def __init__(self, filename, board_size):
        self.filename = filename
        self.board_size = board_size

    def getNumeric(self, letter):
        return ord(letter) - 97

    def convert(self):
        class Turn:
            W = 0
            B = 1

        # open file of games. read one game
        with open(filename) as f_in:
            lines = (line.rstrip() for line in f_in)
            lines = list(line for line in lines if line)  # Non-blank lines in a list

        # print name of the player
        name = lines[0]
        print("Player Name: {}".format(name))
        lines.remove(lines[0])

        for line in lines:
            # initialize new board for the game with 0's
            Wboard = np.zeros((self.board_size, self.board_size))
            Bboard = np.zeros((self.board_size, self.board_size))
            board = [Wboard, Bboard]

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
                print("its {} turn:".format(turn))
                if locat[0] == self.getNumeric("r"):  # when resign
                    print("user {} left the game".format(turn))
                    continue
                elif locat[0] == self.getNumeric("s"):  # when swap
                    print("user {} swap the game".format(turn))
                    continue
                board[turn][locat[0], locat[1]] = 1
                turn = (turn + 1) % 2
                print(board)

if __name__ == "__main__":
    main()

