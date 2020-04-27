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

def compare(config, num_games):
    games = 0
    first_player_wins = 0
    win_ratio, uncertainty = None, None
    ratios = []
    # while True:
    for i in range(num_games):
        alpha_agent = TreeSearchPredictor(config.search_config, model, new_board(config.size), True, t, T)

        while not winner(alpha_agent.board):
            # alpha turn
            alpha_agent.run(config.iterations)
            value, probabilities = alpha_agent.predict()
            probabilities = fix_probabilities(alpha_agent.board, probabilities)
            print(probabilities)
            alpha_move = best_move(probabilities)
            alpha_agent.make_move(alpha_move)
            # insert move to wolve
            letter, number = alpha_move
            alpha_move = str(num_to_letter[letter]) + str(number + 1)
            print(f'alpha: {alpha_move}')
            wolve.insert_move("white", alpha_move)
            if winner(alpha_agent.board):
                print("alpha win!!!")
                break
            # wolve turn
            wolve_move = wolve.genmove("black")
            if wolve_move == "winner":
                print("wolve win!!!")
                break
            print(f'wolve: {wolve_move}')
            letter = letter_to_num[wolve_move[0]]
            number = int(wolve_move[1:]) - 1
            wolve_move = (letter, number)
            alpha_agent.make_move(wolve_move)
            # print(f'b: {wolve_move}')
            # todo insert wolve move to alpha board
            print(wolve.showboard())


        games += 1
        first_player_wins += 1
        win_ratio = float(first_player_wins) / games
        uncertainty = win_ratio * math.sqrt(win_ratio * (1 - win_ratio) / games)

        ratios.append(win_ratio)

    return ratios


if __name__ == '__main__':
    # multi_compare(CompareConfig(), sys.argv[1], sys.argv[2])
    t = 0.01
    T = 0.01
    model = load_model('/home/shlomo/Documents/zeroHex/agent1_zero_dnn/model')
    wolve = WolveProcess("/home/shlomo/Documents/Hex/build/src/wolve/wolve")
    res = wolve.boardsize("11")
    print(res)
    compare(CompareConfig(), num_games=100)

# print_board(flip(predictors[0].board), move, file=sys.stderr)
# print_board(predictors[0].board, flip_move(move), file=sys.stderr)
# if games > 0:
# print('Win ratio %.2f ± %.2f (%d games)' % (win_ratio, uncertainty, games), file=sys.stderr)
