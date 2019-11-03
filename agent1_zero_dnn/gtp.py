import sys
import io
import os
import numpy

from keras.models import load_model

from config import GtpConfig
from tree_search import TreeSearchPredictor
from game import new_board, flip, flip_move, read_move, write_move, make_move, print_board, winner, best_move


class GtpException(Exception):
    pass


class Player:
    def __init__(self, config, model):
        self.config = config
        self.model = model
        self.commands = {
            'name': self.name,
            'version': self.version,
            'protocol_version': self.protocol_version,
            'known_command': self.known_command,
            'list_commands': self.list_commands,
            'quit': self.quit,
            'boardsize': self.boardsize,
            'clear_board': self.clear_board,
            'play': self.play,
            'undo': self.undo,
            'genmove': self.genmove,
            'showboard': self.showboard,
            'set_time': self.set_time,
            'winner': self.winner,
            'hexgui-analyze_commands': self.analyze,
        }
        self.clear_board()
        # TODO: implement time limit. This is currently unused
        self.move_time = 60

    def run(self):
        while True:
            command = input()
            try:
                sys.stdout.write('= %s\n\n' % self.run_command(command))
            except GtpException as e:
                sys.stdout.write('? %s\n\n' % str(e))
            sys.stdout.flush()

    def run_command(self, command):
        command = command.split()
        name, args = command[0], command[1:]
        if name in self.commands:
            try:
                return self.commands[name](*args)
            except TypeError:
                raise GtpException('Wrong number of arguments')
        else:
            raise GtpException('Unrecognized command')

    def name(self):
        return 'HexNet'

    def version(self):
        return '0.1'

    def protocol_version(self):
        return '2'

    def known_command(self, command):
        return 'true' if command in self.commands else 'false'

    def list_commands(self):
        return '\n'.join(self.commands.keys())

    def quit(self):
        sys.exit(0)

    def boardsize(self, boardsize, boardsize1):
        try:
            boardsize, boardsize1 = map(int, (boardsize, boardsize1))
        except:
            raise GtpException('Board size must be an integer')
        if boardsize != self.config.size or boardsize1 != self.config.size:
            raise GtpException('Size is not supported')
        self.clear_board()
        return ''

    def clear_board(self):
        self.board = new_board(self.config.size)
        self.history = []
        return ''

    def play(self, player, move):
        move = read_move(move)
        self.history.append(numpy.copy(self.board))
        if player == 'black':
            self.board = flip(make_move(self.board, move))
        elif player == 'white':
            self.board = make_move(flip(self.board), flip_move(move))
        else:
            self.history.pop()
            raise GtpException('Player is invalid')
        return ''

    def undo(self):
        try:
            self.board = self.history.pop()
        except:
            raise GtpException('No previous moves')
        return ''

    def genmove(self, player):
        if winner(self.board) or winner(flip(self.board)):
            raise GtpException('Game is over')
        self.history.append(self.board)
        if player == 'black':
            # TODO: reuse previous calculations from the MCTS
            predictor = TreeSearchPredictor(self.config.search_config, self.model, self.board, not self.history)
            predictor.run(self.config.iterations)
            value, probabilities = predictor.predict()
            move = best_move(probabilities)
            self.board = flip(make_move(self.board, move))
        elif player == 'white':
            predictor = TreeSearchPredictor(self.config.search_config, self.model, flip(self.board), not self.history)
            predictor.run(self.config.iterations)
            value, probabilities = predictor.predict()
            move = best_move(probabilities)
            self.board = make_move(flip(self.board), move)
            move = flip_move(move)
        else:
            self.history.pop()
            raise GtpException('Player is invalid')
        print('Estimated value: %.2f' % value, file=sys.stderr)
        return write_move(move)

    def showboard(self):
        output = io.StringIO()
        print_board(self.board, file=output)
        result = output.getvalue().strip()
        output.close()
        return result

    def set_time(self, time):
        try:
            time = int(time)
        except ValueError:
            raise GtpException('Time limit must be an integer')
        self.move_time = time
        return ''

    def winner(self):
        if winner(self.board):
            return 'white'
        elif winner(flip(self.board)):
            return 'black'
        else:
            return 'none'

    def analyze(self):
        return ''


if __name__ == '__main__':
    config = GtpConfig()
    model = load_model(os.path.dirname(os.path.realpath(__file__)) + '/output/model')
    player = Player(config, model)
    player.run()
