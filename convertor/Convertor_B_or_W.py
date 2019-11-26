# script gets HEX games in letters like: W[aa];B[bb];W[cd];B[dd])
# prints the board in every step
import numpy as np
filename = "1630.txt"

def main():
    c = Convertor(filename, 11)
    c.convert()

class Convertor:
    def __init__(self, filename, board_size):
        self.filename = filename
        self.board_size = board_size

    def getNumeric(self, letter):
        return ord(letter) - 97

    def check_size(self, sp_line):
        valid_size = "SZ[11]"
        game_info = sp_line[0]
        if valid_size in game_info:
            return True
        else:
            return False

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
        # remove first line
        lines.remove(lines[0])

        file = open("test_file.txt", "w")

        for line in lines:
            # organize locations
            sp_line = line.split(";")
            sp_line.remove(sp_line[0])

            # check if game is size 11
            if self.check_size(sp_line):
                Game_info = sp_line[0]
                # check if ower player is W or B in the specific game
                W_name = "PW[{}]".format(name)
                F_or_S = "S"
                if W_name in Game_info:
                    F_or_S = "F"
                    print("Player is W (first)")

                sp_line.remove(sp_line[0])
                # initialize new board for the game with 0's
                Wboard = np.zeros((self.board_size, self.board_size))
                Bboard = np.zeros((self.board_size, self.board_size))
                board = [Wboard, Bboard]

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

                    # print only player moves
                    if F_or_S == "F":
                        if turn == Turn.W:
                             print(board)
                             file.write(board.__str__())
                        board[turn][locat[0], locat[1]] = 1
                        file.write("\n")
                        if turn == Turn.W:
                             file.write(board.__str__())
                             file.write("\nnext move:")
                             print(board)
                        turn = (turn + 1) % 2
                    else:
                        if turn == Turn.B:
                             file.write(board.__str__())
                             print(board)
                        board[turn][locat[0], locat[1]] = 1
                        file.write("\n")
                        if turn == Turn.B:
                             file.write(board.__str__())
                             file.write("\nnext move:")
                             print(board)
                        turn = (turn + 1) % 2
                file.write("\nnext game:\n")
            # if its not 11 size game continue to next line
            else:
                continue

if __name__ == "__main__":
    main()

