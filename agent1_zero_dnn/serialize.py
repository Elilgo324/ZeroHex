import numpy

from struct import Struct

from agent1_zero_dnn.game import new_board

short = Struct('H')
boolean = Struct('?')

def record_size(size):
    return size * size * 2 + 1

def read_record(f, size):
    record = f.read(record_size(size))
    board = new_board(size)
    visits = numpy.zeros((size, size))
    offset = 0
    for x in range(size):
        for y in range(size):
            cell = short.unpack_from(record, offset)[0]
            offset += short.size
            board[0,x,y] = (cell >> 6) & 1
            board[1,x,y] = (cell >> 7) & 1
            visits[x,y] = cell & ((1 << 6) - 1)
    won = boolean.unpack_from(record, offset)[0]
    return board, won, visits

def write_record(f, board, won, visits):
    size = board.shape[1]
    record = bytearray(record_size(size))
    offset = 0
    for x in range(size):
        for y in range(size):
            first_player = int(board[0,x,y])
            second_player = int(board[1,x,y])
            cell_visits = int(visits[x,y])
            short.pack_into(record, offset, (first_player << 6) | (second_player << 7) | cell_visits)
            offset += short.size
    boolean.pack_into(record, offset, won)
    f.write(record)
