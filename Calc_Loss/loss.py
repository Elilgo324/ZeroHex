
from agent1_zero_dnn.compare import *
from convertor.Convertor_ver3 import convert
from convertor.Convertor_ver3 import convert_last_moves
from agent1_zero_dnn.game import ori_moves, best_k_moves
from agent1_zero_dnn.generate import fix_probabilities
import sys
import numpy as np
import os
# file_name = "data_text_games_name_in_first_line/2688.txt"
# file_name = "data_text_games_name_in_first_line/2508.txt"
# file_name = "data_text_games_name_in_first_line/2062.txt"
model_file1 = "agent1_zero_dnn/model"
config = CompareConfig()
# moves = convert(file_name)

model = load_model(model_file1)
predictor = TreeSearchPredictor(config.search_config, model, new_board(config.size), True)
temp = 0.7


def calc_file(file_name):
    predictor.is_first_move = False
    win, lose = 0, 0
    res = str()
    moves = convert(file_name)
    for mv in moves:
        # insert board to predictor
        # predictor.board = np.array(mv.board_stt)
        if mv.color == 'B':
            predictor.board = np.array(mv.board_stt)
        elif mv.color == 'W':
            predictor.board = np.array(flip_move(mv.board_stt))
        predictor.run(config.iterations)
        # predict
        value, probabilities = predictor.predict()
        probabilities = fix_probabilities(predictor.board, probabilities)
        # print(probabilities)
        tprobs = temperature(probabilities, temp)
        next_move = mv.next_mv[0], mv.next_mv[1]
        # get 15 different moves from model
        # todo tprobs in ori moves
        model_moves = best_k_moves(probabilities, 20)
        predictor.make_move(next_move)
    #    model_moves = ori_moves(probabilities, 15)
    #     print('user {}'.format(next_move))
    #     print('model {}'.format(model_moves))
        # check if user's move in prediction
        if next_move in model_moves:
            win += 1
            res += 'w'
        else:
            lose += 1
            res += 'l'
    print('wins: %d' % win)
    print('lose: %d' % lose)
    if moves.__len__() != 0:
        print('ratio: %s' % (win/(win+lose)))
    print(res)
    print('-----------------------------')
# print_board(predictor.board, flip_move(next_move), file=sys.stderr)


if __name__ == '__main__':
    files = os.listdir('data_text_games_name_in_first_line')
    files = ['2508.txt']
    for file in files:
        print(file)
        calc_file('data_text_games_name_in_first_line/' + file)


