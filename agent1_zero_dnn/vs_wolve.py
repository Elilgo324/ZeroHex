import sys
import math
from keras.models import load_model
from agent1_zero_dnn.game import print_board, winner, flip, flip_move, best_move, new_board, sample_move, shlomo_move
from agent1_zero_dnn.tree_search import TreeSearchPredictor, temperature
from agent1_zero_dnn.config import CompareConfig
import subprocess


def compare(config, num_games):
    games = 0
    first_player_wins = 0
    win_ratio, uncertainty = None, None

    ratios = []
    # while True:
    for i in range(num_games):
        alpha_agent = TreeSearchPredictor(config.search_config, model1, new_board(config.size), True, t, T)
        # wolve_proc = subprocess.Popen("wolve command")
        # input, output = wolve_proc.communicate()

        while not winner(alpha_agent.board):
            # alpha turn
            alpha_agent.run(config.iterations)
            value, probabilities = alpha_agent.predict()
            move = shlomo_move(probabilities)
            alpha_agent.make_move(move)
            if winner(alpha_agent.board):
                print("alpha win!!!")
                break
            # wolve turn
            # those lines are pseudo code
            # send alpha move to wolve
            # ask wolve to genmove black
            # get wolve response and insert it to alpha_agent.board
            # check if wolve won
            # end of loop


        games += 1
        first_player_wins += 1
        win_ratio = float(first_player_wins) / games
        uncertainty = win_ratio * math.sqrt(win_ratio * (1 - win_ratio) / games)

        ratios.append(win_ratio)

    return ratios


if __name__ == '__main__':
    # multi_compare(CompareConfig(), sys.argv[1], sys.argv[2])
    t = 0.1
    T = 0.001
    model1, model2 = load_model(sys.argv[1]), load_model(sys.argv[2])
    compare(CompareConfig(), num_games=100)

# print_board(flip(predictors[0].board), move, file=sys.stderr)
# print_board(predictors[0].board, flip_move(move), file=sys.stderr)
# if games > 0:
# print('Win ratio %.2f ± %.2f (%d games)' % (win_ratio, uncertainty, games), file=sys.stderr)
