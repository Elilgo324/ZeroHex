# script gets HEX games in letters like: W[aa];B[bb];W[cd];B[dd])
# prints the board in every step

from convertor.avshalom_move import Move
import copy

filename = "../data_text_games_name_in_first_line/1667.txt"
# filename = "NEW1999CHANGED.txt"
# filename = "TEST1.txt"
board_size = 11
minimal_game_len = 22
minimal_mv_index = 6

def main():
    p_moves = convert_last_moves(filename)
    for mv in p_moves:
        print(mv)
    print("num of mvs: {}".format(len(p_moves)))


class Turn:
    W = 0
    B = 1

def getNumeric(letter):
    return ord(letter) - 97

def check_size(sp_line):
    valid_size = "SZ[11]"
    game_info = sp_line[0]
    if valid_size in game_info:
        return True
    else:
        return False

def convert(filename):
    # open file of games. read one game
    with open(filename) as f_in:
        lines = (line.rstrip() for line in f_in)
        lines = list(line for line in lines if line)  # Non-blank lines in a list

    # print name of the player
    name = lines[0]
    # remove first line
    lines.remove(lines[0])
    # initialize player moves
    player_moves = []
    # collect moves from every game
    for line in lines:
        # print("{}".format(line))
        game_mvs = get_game_moves(line, name)
        # insert to one big list og player moves
        for p_mv in game_mvs:
            player_moves.append(p_mv)

    return player_moves

def convert_last_moves(filename):
    # open file of games. read one game
    with open(filename) as f_in:
        lines = (line.rstrip() for line in f_in)
        lines = list(line for line in lines if line)  # Non-blank lines in a list

    # print name of the player
    name = lines[0]
    # remove first line
    lines.remove(lines[0])
    # initialize player moves
    player_moves = []
    # collect moves from every game
    for line in lines:
        game_mvs = get_game_moves(line, name)
        # check if there are moves
        if len(game_mvs) != 0:
            last_mv = game_mvs[-1]
            player_moves.append(last_mv)
    return player_moves


def get_locations(sp_line):
    locations = []
    for loc in sp_line:
        x_val = getNumeric(loc[2])
        y_val = getNumeric(loc[3])
        location = [x_val, y_val]
        locations.append(location)
    return locations

def get_game_moves(line, name):
    #initialize this game moves
    game_mvs = []
    # organize locations
    sp_line = line.split(";")
    # throw away garbage
    sp_line.remove(sp_line[0])
    # check if game is size 11
    if check_size(sp_line):
        Game_info = sp_line[0]
        # check if ower player is W or B in the specific game
        W_name = "PW[{}]".format(name)
        BorW = "B"
        if W_name in Game_info:
            BorW = "W"
        # remove game information
        sp_line.remove(sp_line[0])
        # initialize new board for the game with 0's
        Wboard = [[0 for i in range(board_size)] for j in range(board_size)]
        Bboard = [[0 for i in range(board_size)] for j in range(board_size)]
        board = [Wboard, Bboard]

        locations = get_locations(sp_line)
        # only for games grater than 22
        if len(locations) >= minimal_game_len:
            turn = Turn.W
            # modify board
            index_loc = 0
            for locat in locations:
                # takes only moves from 6 and up
                if index_loc < minimal_mv_index:
                    index_loc += 1
                    continue
                if locat[0] == getNumeric("r"):  # when resign
                    continue
                elif locat[0] == getNumeric("s"):  # when swap
                    continue
                # initialize move
                m = Move()
                # save only our player moves
                if BorW == "W":  # our player is White
                    if turn == Turn.W:  # and this is white turn
                        set_clr_bord_stt(m, BorW, board)
                    board[turn][locat[0]][locat[1]] = 1
                    if turn == Turn.W:
                        m.next_mv = locat
                        game_mvs.append(m)
                else:  # our player is Black
                    if turn == Turn.B:  # and this is black turn
                        set_clr_bord_stt(m, BorW, board)
                    board[turn][locat[0]][locat[1]] = 1
                    if turn == Turn.B:
                        m.next_mv = locat
                        game_mvs.append(m)
                turn = (turn + 1) % 2
                index_loc += 1
    return game_mvs

def set_clr_bord_stt(m, BorW, board):
    m.color = BorW
    m.board_stt = copy.deepcopy(board)


if __name__ == "__main__":
    main()
