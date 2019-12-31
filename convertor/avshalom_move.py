class Move:
    def __init__(self, color=None, board_stt=None, next_mv=None):
        self.color = color
        self.board_stt = board_stt
        self.next_mv = next_mv

    def __repr__(self):
        return str([self.color, self.board_stt, self.next_mv])