import sys
import math
from keras.models import load_model
from agent1_zero_dnn.game import print_board, winner, flip, flip_move, best_move, new_board, sample_move, shlomo_move, fix_probabilities
from agent1_zero_dnn.tree_search import TreeSearchPredictor, temperature
from agent1_zero_dnn.config import CompareConfig

from agent1_zero_dnn.wolve_integration import WolveProcess

num_to_letter = {
    0: "a",
    1: "b",
    2: "c",
    3: "d",
    4: "e",
    5: "f",
    6: "g",
    7: "h",
    8: "i",
    9: "j",
    10: "k",
    11: "l"
}

letter_to_num = {
    "a": 0,
    "b": 1,
    "c": 2,
    "d": 3,
    "e": 4,
    "f": 5,
    "g": 6,
    "h": 7,
    "i": 8,
    "j": 9,
    "k": 10,
    "l": 11
}


def compare(config, num_games, temp, Temp, name):
    print('\nplaying with', name, 'with vals:', temp, Temp)
    alpha_wins = 0
    wolve_wins = 0

    # while True:
    for i in range(num_games):
        # alpha_agent = TreeSearchPredictor(config.search_config, model, new_board(config.size), True, t, T)
        alpha_agent = TreeSearchPredictor(config.search_config, model, new_board(config.size), True, temp, Temp)

        # make sure wolve have new clear board
        wolve.clear_board()
        # start game
        print('its game number: ', i+1)


        while not winner(alpha_agent.board):
            # alpha turn
            alpha_agent.run(config.iterations)
            value, probabilities = alpha_agent.predict()
            #print(probabilities)
            #probabilities = fix_probabilities(alpha_agent.board, probabilities)
            probabilities = fix_probabilities(alpha_agent.board, probabilities)
            #print(probabilities)
            alpha_move = best_move(probabilities)
            #print('alphaaaaa: ', alpha_move)
            alpha_agent.make_move(alpha_move)
            # insert move to wolve
            letter, number = alpha_move
            alpha_move = str(num_to_letter[letter]) + str(number + 1)
            #print(f'alpha(B): {alpha_move}')
            wolve.insert_move("black", alpha_move)
            if winner(alpha_agent.board):
                print("alpha wins!!!")
                alpha_wins += 1
                continue
            # wolve turn
            wolve_move = wolve.genmove("white")
            #print(f'wolve(W): {wolve_move}')
            letter = letter_to_num[wolve_move[0]]
            number = int(wolve_move[1:]) - 1
            #wolve_move = (letter, number)
            wolve_move = (number, letter)
            # insert wolve move to alpha
            alpha_agent.make_move(wolve_move)
            #print('wove board:')
            #print(wolve.showboard())
            # print('alpha board:')
            # print_board(flip(alpha_agent.board), wolve_move, file=sys.stderr)
            if winner(alpha_agent.board):
                print("wolve wins!!!")
                wolve_wins += 1
                continue

        print(name, 'won', alpha_wins, 'out of', i + 1)
        print('wolve won', wolve_wins, 'out of', i + 1)


    print(name, 'won', alpha_wins, 'times out of', num_games, 'games')
    print('wolve won', wolve_wins, 'times out of', num_games, 'games')
    return alpha_wins/num_games


if __name__ == '__main__':
    # multi_compare(CompareConfig(), sys.argv[1], sys.argv[2])
    model = load_model('/home/avshalom/PycharmProjects/zeroHex/agent1_zero_dnn/model')
    # /home/avshalom/PycharmProjects/benzene-vanilla-cmake
    wolve = WolveProcess("/home/avshalom/PycharmProjects/benzene-vanilla-cmake/build/src/wolve/wolve")
    res = wolve.boardsize("11")
    # limit wolves thinking
    wolve.param_wolve('max_time', 0.0001)
    wolve.param_wolve('max_depth', 1)
    wolve.param_wolve('use_cache_book', 0)
    wolve.param_wolve('ply_width', 1)
    wolve.param_wolve('tt_bits', 2)
    # competition
    num_games = 10
    players_arr = [[0.01, 0.01, 'Lisa'], [0.24, 0.08, 'Bart'], [0.44, 0.3, 'Maggie'], [0.49, 0.38, 'Homer']]

    for player in players_arr:
        wolve_vic = compare(CompareConfig(), num_games, player[0], player[1], player[2])
        print(player[2], 'percent is: ', wolve_vic*100, '%')



'''
param_wolve
= 
[bool] backup_ice_info 1
[bool] ponder 0
[bool] use_cache_book 1
[bool] use_guifx 0
[bool] search_singleton 0
[bool] use_parallel_solver 0
[bool] use_time_management 0
[bool] use_early_abort 0
[string] ply_width 15
[string] specific_ply_widths ""
[string] max_depth 99
[string] max_time 10
[string] min_depth 1
[string] tt_bits 20
'''
# print_board(flip(predictors[0].board), move, file=sys.stderr)
# print_board(predictors[0].board, flip_move(move), file=sys.stderr)
# if games > 0:
# print('Win ratio %.2f ± %.2f (%d games)' % (win_ratio, uncertainty, games), file=sys.stderr)

    # print('wolve move at alpha is:' + str(wolve_move))
            # print_board(alpha_agent.board, (-1, -1), file=sys.stderr)
            # print_board(alpha_agent.board, flip_move(wolve_move), file=sys.stderr)
            # print_board(flip(alpha_agent.board), flip_move(wolve_move), file=sys.stderr)