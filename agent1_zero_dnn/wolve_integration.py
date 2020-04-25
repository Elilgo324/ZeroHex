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
        #print(self.proc.stdout.read(6).decode())
        output = self.proc.stdout.read(6).decode()
        self.proc.stdout.flush()
        move = output.split("= ")[-1].strip()
        #print(output)
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
        #print(self.proc.stdout.read(4).decode())
        output = self.proc.stdout.read(4).decode()
        self.proc.stdout.flush()
        return "=" in output

    def close(self):
        self.proc.stdin.close()
        self.proc.terminate()
        self.proc.wait(timeout=0.2)


if __name__ == '__main__':
    wolve = WolveProcess('/home/avshalom/PycharmProjects/benzene-vanilla-cmake/build/src/wolve/wolve')
    wolve.boardsize(11)
    print(wolve.showboard())
    # lets say alpha generated a1 move - play w a1 to wolve
    wolve.insert_move('w', 'a1')
    # wolve turn
    m1 = wolve.genmove('b')
    print(wolve.showboard())
    # alpha turn
    wolve.insert_move('w', 'c10')
    # wolve move
    m2 = wolve.genmove('b')
    print(wolve.showboard())


