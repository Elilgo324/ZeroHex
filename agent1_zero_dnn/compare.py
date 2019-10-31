import sys
import math

from keras.models import load_model

from game import print_board, winner, flip, flip_move, best_move, new_board, sample_move
from tree_search import TreeSearchPredictor
from config import CompareConfig


def compare(config, model_file1, model_file2):
    models = [load_model(model_file1), load_model(model_file2)]
    games = 0
    first_player_wins = 0
    win_ratio, uncertainty = None, None
    # while True:
    for i in range(151):
        move_index = 0
        predictors = [TreeSearchPredictor(config.search_config,model,new_board(config.size),True) for model in models]

        # exp uct of model2 is 100
        # predictors = ["avshalom", "shlomo"]
        # predictors[0] = TreeSearchPredictor(config.search_config, models[0], new_board(config.size), True)
        # config.search_config.uct_factor = 100.0
        # predictors[1] = TreeSearchPredictor(config.search_config, models[1], new_board(config.size), True)

        while not winner(predictors[0].board):
            if move_index == 0:
                predictor = predictors[1]
            else:
                predictor = predictors[(games ^ move_index) & 1]
            predictor.run(config.iterations)
            value, probabilities = predictor.predict()

            # exp uniform probs for model2
            # uprobs = [0.00826446] * 121
            # if move_index == 0:
            #    probabilities = uprobs

            if move_index < 3:
                move = sample_move(probabilities)
            else:
                move = best_move(probabilities)
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


if __name__ == '__main__':
    compare(CompareConfig(), sys.argv[1], sys.argv[2])
