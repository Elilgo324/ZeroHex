import sys
import math
import numpy as np

from keras.models import load_model

from agent1_zero_dnn.game import print_board, winner, flip, flip_move, best_move, new_board, sample_move, shlomo_move
from agent1_zero_dnn.tree_search import TreeSearchPredictor, temperature
from agent1_zero_dnn.config import CompareConfig

import matplotlib.pyplot as plt


def multi_compare(config, model_file1, model_file2):
    #temps = [0.7, 0.8, 0.85, 0.9, 0.95, 1]
    temps = [0.7, 0.9]
    num_games = 3

    plt.style.use('seaborn-darkgrid')
    plt.ylim(0, 1)
    plt.title("Temperature Modification", loc='left', fontsize=12, fontweight=0, color='orange')
    plt.xlabel('Games')
    plt.ylabel('Win Ratio')
    plt.legend(bbox_to_anchor=(0.,1.02,1.,.102),loc='lower left',
               ncol=2,mode="expand",borderaxespad=0.)

    for t in temps:
        ratios = compare(config, model_file1, model_file2, t, num_games)
        plt.plot(range(num_games), ratios, label=str(t))

    plt.savefig('temps.png')
    #plt.show()


def compare(config, model_file1, model_file2, temp, num_games):
    models = [load_model(model_file1), load_model(model_file2)]
    games = 0
    first_player_wins = 0
    win_ratio, uncertainty = None, None

    ratios = []
    # while True:
    for i in range(num_games):
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
            tprobs = temperature(probabilities, temp)
            if games & 1 == move_index & 1:
                probabilities = tprobs
                #print(probabilities)

            if move_index < 3:
                move = shlomo_move(probabilities)
            else:
                #move = best_move(probabilities)
                move = shlomo_move(probabilities)
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

    return ratios


if __name__ == '__main__':
    multi_compare(CompareConfig(), sys.argv[1], sys.argv[2])
    #compare(CompareConfig(), sys.argv[1], sys.argv[2])

