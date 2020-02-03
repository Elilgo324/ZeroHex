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


model_name="model"
config = CompareConfig()
model=load_model(model_name)
predictor = TreeSearchPredictor(config.search_config, model, new_board(config.size), True)


def update_temp(x,y,w,m=0,v=0):
    """
    deriev loss according params
    deraive 1-0 loss according temp
    :param loss:
    :return:
    """
    num_iterations = 10000
    epsilon = 1e-08
    beta_1 = 0.9
    beta_2 = 0.999
    step_size = 0.001

    for t in range(num_iterations):
        g = compute_gradient(x, y)
        m = beta_1 * m + (1 - beta_1) * g
        v = beta_2 * v + (1 - beta_2) * np.power(g, 2)
        m_hat = m / (1 - np.power(beta_1, t))
        v_hat = v / (1 - np.power(beta_2, t))
        w = w - step_size * m_hat / (np.sqrt(v_hat) + epsilon)

    return None


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
    rate = 0.001
    e_t = 1
    e_T = 0.01

    #players = os.listdir('../data_text_games_name_in_first_line')
    players = ["../data_text_games/2300.txt"]
    for player in players:
        moves = convert(player)
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

            t -= rate * t_grad
            T -= rate * T_grad
            print("t: "+str(t)+" ..... T: "+str(T))
    return t,T           


def get_index_from_move(move):
    yx,yy = move.next_mv
    index = 11 * yy + yx
    return index

if __name__ == '__main__':
    learning()
