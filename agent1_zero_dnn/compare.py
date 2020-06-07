import sys
import math
import numpy as np

from keras.models import load_model

from agent1_zero_dnn.game import print_board, winner, flip, flip_move, best_move, new_board, sample_move, refined_move
from agent1_zero_dnn.tree_search import TreeSearchPredictor, temperature
from agent1_zero_dnn.config import CompareConfig

import matplotlib.pyplot as plt


def multi_compare(config, model_file1, model_file2):
    # flip between t and T
    t = np.arange(0.8, 0.999, 0.01).tolist()
    T = [1] * 20
    t = [0.01,0.1,0.2,0.3,0.4,0.5]
    T = [1,1,1,1,1,1]
    param = "t"
    plt_param = t

    num_games = 100

    plt.style.use('seaborn-darkgrid')
    plt.ylim(0, 1)
    plt.title(param +" modification", loc='left', fontsize=24, fontweight=2, color='orange')
    plt.xlabel(param+' values')
    plt.ylabel('win ratio')
    plt.legend(bbox_to_anchor=(0.,1.02,1.,.102),loc='lower left',
               ncol=2,mode="expand",borderaxespad=0.)

    model1, model2 = load_model(model_file1), load_model(model_file2)

    ratios = []
    for _t,_T in zip(t,T):
        r = compare(config,model1,model2,_t,_T,num_games)
        print("t="+str(_t)+",T="+str(_T)+","+str(r[len(r)-1]))
        ratios.append(r[len(r)-1])

    plt.plot(plt_param,ratios,marker='o',linestyle='--',color='r',label='Square')
    plt.savefig(param+'.png')
    plt.show()


def compare(config, model1, model2, t, T, num_games):
    games = 0
    first_player_wins = 0
    win_ratio, uncertainty = None, None

    ratios = []
    for i in range(num_games):
        move_index = 0
        predictors = [TreeSearchPredictor(config.search_config,model1,new_board(config.size),True, t, T)
            ,TreeSearchPredictor(config.search_config,model2,new_board(config.size),True)]

        while not winner(predictors[0].board):
            if move_index == 0:
                predictor = predictors[1]
            else:
                predictor = predictors[(games ^ move_index) & 1]
            predictor.run(config.iterations)
            value, probabilities = predictor.predict()

            if games & 1 == move_index & 1:
                probabilities = temperature(probabilities,T)

            move = refined_move(probabilities)

            for predictor in predictors:
                predictor.make_move(move)

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


