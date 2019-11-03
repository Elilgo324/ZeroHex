import sys
import math
import numpy as np

from keras.models import load_model

from game import print_board, winner, flip, flip_move, best_move, new_board, sample_move
from tree_search import TreeSearchPredictor
from config import CompareConfig

import matplotlib.pyplot as plt


def temperature(probs, t):
    probs = np.array(probs)
    probs = np.power(probs, 1/t) / np.sum(np.power(probs, 1/t))
    return probs


def compare(config, model_file1, model_file2):
    models = [load_model(model_file1), load_model(model_file2)]
    games = 0
    first_player_wins = 0
    win_ratio, uncertainty = None, None

    ratios = []
    # while True:
    for i in range(10):
        move_index = 0
        predictors = [TreeSearchPredictor(config.search_config,model,new_board(config.size),True) for model in models]

        # exp uct of model2 is 100
        # predictors = ["avshalom", "shlomo"]
        # config.search_config.uct_factor = 5.0
        # predictors[0] = TreeSearchPredictor(config.search_config, models[0], new_board(config.size), True)
        # config.search_config.uct_factor = 100.0
        # predictors[1] = TreeSearchPredictor(config.search_config, models[1], new_board(config.size), True)

        # exp uct of model2 is 100
        # predictors = ["avshalom", "shlomo"]
        # config.search_config.uct_factor = 5.0
        # predictors[0] = TreeSearchPredictor(config.search_config, models[0], new_board(config.size), True)
        # config.search_config.uct_factor = 100.0
        # predictors[1] = TreeSearchPredictor(config.search_config, models[1], new_board(config.size), True)

        # exp virtual loss of model2 is 100
        # predictors = ["avshalom", "shlomo"]
        # config.search_config.virtual_loss = 3.0
        # predictors[0] = TreeSearchPredictor(config.search_config, models[0], new_board(config.size), True)
        # config.search_config.virtual_loss = 100.0
        # predictors[1] = TreeSearchPredictor(config.search_config, models[1], new_board(config.size), True)

        # exp virtual loss of model2 is 0
        # predictors = ["avshalom", "shlomo"]
        # config.search_config.virtual_loss = 3.0
        # predictors[0] = TreeSearchPredictor(config.search_config, models[0], new_board(config.size), True)
        # config.search_config.virtual_loss = 0
        # predictors[1] = TreeSearchPredictor(config.search_config, models[1], new_board(config.size), True)

        while not winner(predictors[0].board):
            if move_index == 0:
                predictor = predictors[1]
            else:
                predictor = predictors[(games ^ move_index) & 1]
            predictor.run(config.iterations)
            value, probabilities = predictor.predict()

            # exp uniform probs
            #uprobs = [0.00826446] * 121
            #if games & 1 == move_index & 1:
            #   probabilities = np.array(uprobs).reshape(11, -1)

            # exp temperature
            tprobs = temperature(probabilities, 10000)
            if games & 1 == move_index & 1:
                probabilities = tprobs
                #print(probabilities)

            if move_index < 3:
                move = sample_move(probabilities)
            else:
                #move = best_move(probabilities)
                move = sample_move(probabilities)
            for predictor in predictors:
                predictor.make_move(move)
            if games & 1 == move_index & 1:
                print_board(flip(predictors[0].board), move, file=sys.stderr)
            else:
                print_board(predictors[0].board, flip_move(move), file=sys.stderr)
            print('%s model win probability: %.2f' % (['First', 'Second'][((games ^ move_index) & 1)], (value + 1) / 2), file=sys.stderr)
            if games > 0:
                print('Win ratio %.2f ± %.2f (%d games)' % (win_ratio, uncertainty, games), file=sys.stderr)
            move_index += 1
        games += 1
        if games & 1 == move_index & 1:
            first_player_wins += 1
        win_ratio = float(first_player_wins) / games
        uncertainty = win_ratio * math.sqrt(win_ratio * (1 - win_ratio) / games)

        ratios.append(win_ratio)

    # plot ratio graph (first_player_wins / games)
    plt.plot(range(games),ratios)
    plt.ylim(0, 1)
    plt.xlabel('games')
    plt.ylabel('ratio')
    plt.show()

    print(ratios)


if __name__ == '__main__':
    compare(CompareConfig(), sys.argv[1], sys.argv[2])
