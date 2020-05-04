from subprocess import Popen, PIPE


class WolveProcess:

    def __init__(self, path) -> None:
        self.proc = Popen([path], stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=False)

    def insert_move(self, color, move):
        command = f'play {color} {move}\n'.encode()
        self.proc.stdin.write(command)
        self.proc.stdin.flush()
        output = self.proc.stdout.read(4).decode()
        self.proc.stdout.flush()
        return "=" in output

    def genmove(self, color):
        command = f'genmove {color}\n'.encode()
        self.proc.stdin.write(command)
        self.proc.stdin.flush()
        #output = self.proc.stdout.read(6).decode()
        output = self.proc.stdout.readline().decode()
        output2 = self.proc.stdout.readline().decode()
        self.proc.stdout.flush()
        move = output.split("= ")[-1].strip()
        if move[0] == 'r':
            return "winner"
        else:
            return move

    def showboard(self):
        command = 'showboard\n'.encode()
        self.proc.stdin.write(command)
        self.proc.stdin.flush()
        output = self.proc.stdout.read(573).decode()
        self.proc.stdout.flush()
        return output

    def boardsize(self, size):
        command = f'boardsize {size}\n'.encode()
        self.proc.stdin.write(command)
        self.proc.stdin.flush()
        output = self.proc.stdout.read(4).decode()
        self.proc.stdout.flush()
        return "=" in output

    def clear_board(self):
        command = f'clear_board\n'.encode()
        self.proc.stdin.write(command)
        self.proc.stdin.flush()
        output = self.proc.stdout.read(4).decode()
        self.proc.stdout.flush()
        return "=" in output

    def param_wolve(self, lim_type, lim_val):
        command = f'param_wolve {lim_type} {lim_val}\n'.encode()
        self.proc.stdin.write(command)
        self.proc.stdin.flush()
        output = self.proc.stdout.read(4).decode()
        self.proc.stdout.flush()
        return "=" in output

    def close(self):
        self.proc.stdin.close()
        self.proc.terminate()
        self.proc.wait(timeout=0.2)


if __name__ == '__main__':
    #players_arr = [[0.01, 0.01, 'Lisa'], [0.24, 0.08, 'Bart']]

    wolve = WolveProcess('/home/avshalom/PycharmProjects/benzene-vanilla-cmake/build/src/wolve/wolve')
    wolve.boardsize(11)

    wolve.param_wolve('max_time', 0.05)
    wolve.param_wolve('max_depth', 2)
    wolve.param_wolve('use_cache_book', 0)

    print(wolve.showboard())
    # lets say alpha generated a1 move - play w a1 to wolve
    wolve.insert_move('b', 'a1')
    print(wolve.showboard())
    # wolve turn
    wolve.genmove('w')
    print(wolve.showboard())
    # alpha turn
    wolve.insert_move('b', 'a2')
    # wolve move
    wolve.genmove('w')
    print(wolve.showboard())
    wolve.insert_move('b', 'a3')
    # wolve move
    wolve.genmove('w')
    print(wolve.showboard())


    '''
    param_wolve
    = 
    [bool] backup_ice_info 1
    [bool] ponder 0
    [bool] use_cache_book 1
    [bool] use_guifx 0
    [bool] search_singleton 0
    [bool] use_parallel_solver 0
    [bool] use_time_management 0
    [bool] use_early_abort 0
    [string] ply_width 15
    [string] specific_ply_widths ""
    [string] max_depth 99
    [string] max_time 10
    [string] min_depth 1
    [string] tt_bits 20
    '''
