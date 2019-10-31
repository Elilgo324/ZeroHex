import random
import sys
import time
import numpy

from keras.models import load_model

from tree_search import TreeSearchPredictor
from serialize import write_record, record_size
from game import new_board, winner, make_move, print_board, fix_probabilities, sample_move
from config import GenerateConfig

def game_result(config, model, moves):
    last_move_index = len(moves) - 1
    end = random.randint(0, last_move_index)
    board = new_board(config.size)
    for move in moves[:end]:
        board = make_move(board, move)
    predictor = TreeSearchPredictor(config.search_config, model, board, end == 0)
    predictor.run(config.iterations)
    return board, last_move_index % 2 == end % 2, predictor.visits()

def generate(config, model_file, output_file):
    model = load_model(model_file)
    with open(output_file, 'ab') as fout:
        file_pos = fout.tell()
        # Truncate any partially written record
        fout.seek(file_pos - file_pos % record_size(config.size))
        samples = 0
        start_time = time.time()
        game_boards = numpy.array([new_board(config.size) for i in range(config.batch_size)])
        game_moves = [[] for i in range(config.batch_size)]
        while True:
            _values, priors = model.predict(game_boards)
            priors = numpy.reshape(priors, (-1, config.size, config.size))
            for i in range(config.batch_size):
                probs = fix_probabilities(game_boards[i], priors[i])
                move = sample_move(probs)
                game_moves[i].append(move)
                game_boards[i] = make_move(game_boards[i], move)
                if winner(game_boards[i]):
                    samples += 1
                    board, won, visits = game_result(config, model, game_moves[i])
                    write_record(fout, board, won, visits)
                    fout.flush()
                    print_board(board, file=sys.stderr)
                    print('Games: %d, Time per game: %.2fs' % (samples, (time.time() - start_time) / samples), file=sys.stderr)
                    game_boards[i] = new_board(config.size)
                    game_moves[i] = []

if __name__ == '__main__':
    generate(GenerateConfig(), sys.argv[1], sys.argv[2])
