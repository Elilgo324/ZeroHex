import numpy as np
from agent1_zero_dnn.compare import *
from agent1_zero_dnn.tree_search import TreeSearchPredictor,temperature
from convertor.Convertor_ver4 import convert
from convertor.Convertor_ver4 import convert_last_moves
from agent1_zero_dnn.game import ori_moves,best_k_moves,new_board
from agent1_zero_dnn.generate import fix_probabilities
import sys
import numpy as np
import os
from agent1_zero_dnn.config import CompareConfig
import math


model_name="model"
config = CompareConfig()
model=load_model(model_name)
predictor = TreeSearchPredictor(config.search_config, model, new_board(config.size), True)


def adam(params,grads,lr,vs,sqrs,i):
    beta1 = 0.9
    beta2 = 0.999
    eps_stable = 1e-8
    ret_params = []

    for param,grad,v,sqr in zip(params,grads,vs,sqrs):
        g = grad

        v = beta1 * v + (1. - beta1) * g
        sqr = beta2 * sqr + (1. - beta2) * np.square(g)

        v_bias_corr = v / (1. - beta1 ** i)
        sqr_bias_corr = sqr / (1. - beta2 ** i)

        div = lr * v_bias_corr / (math.sqrt(sqr_bias_corr) + eps_stable)
        ret_params.append(param - div)
    return ret_params


def compute_gradient(x, y):
    return 0

def neglog_loss(x, y):
    epsilon = 0.00001
    return -math.log(x[y]+epsilon)
    #return -math.log(x[y]*3+epsilon)

def loss(x,y):
    N = 15
    res = sorted(range(len(x)),key=lambda sub: x[sub])[-N:]
    if y in res:
        return 0
    epsilon = 0.00001
    return -math.log(x[y] + epsilon)

def learning():
    # params
    t = 1
    T = 1

    # hyper params
    lr = 0.001
    e_t = 0.01
    e_T = 0.01

    i = 0
    vs,sqrs = [0,0],[0,0]
    players = os.listdir('../bert')
    #players = ["../data_text_games/2300.txt"]
    for player in players:
        moves = convert("../data_text_games/" + str(player))
        for move in moves:
            predictor.board = np.array(move.board_stt)
            predictor.is_first_move = False
            predictor.run(config.iterations)

            # probs
            predictor.t = t
            _,probs = predictor.predict()
            x = temperature(fix_probabilities(predictor.board,probs), T).reshape(121)

            # probs with close t
            predictor.t = t+e_t
            _,e_probs = predictor.predict()
            et_x = temperature(fix_probabilities(predictor.board,e_probs), T).reshape(121)

            # probs with close T
            predictor.t = t
            _,e_probs = predictor.predict()
            eT_x = temperature(fix_probabilities(predictor.board,e_probs), T + e_T).reshape(121)

            # true move
            y = get_index_from_move(move)

            # numeric gradient
            t_grad = (loss(x,y) - loss(et_x,y)) / e_t
            T_grad = (loss(x,y) - loss(eT_x,y)) / e_T

            grads = [t_grad,T_grad]
            params = [t,T]
            i += 1
            t,T = adam(params,grads,lr,vs,sqrs,i)

            print("t: "+str(t)+" ..... T: "+str(T))
    return t,T           


def get_index_from_move(move):
    yx,yy = move.next_mv
    index = 11 * yy + yx
    return index

if __name__ == '__main__':
    learning()
