import math
import numpy
import asyncio

from game import winner, make_move, normalize
from batch_predictor import BatchPredictor

class TreeSearchPredictor:
    def __init__(self, config, model, board, is_first_move):
        self.config = config
        self.model = model
        self.predictor = BatchPredictor(model)
        self.board = board
        self.is_first_move = is_first_move
        self._create_root()

    def run(self, iterations):
        loop = asyncio.get_event_loop()
        for i in range(iterations):
            coroutines = []
            self.predictor.start_batch(self.config.batch_size)
            for j in range(self.config.batch_size):
                coroutines.append(self.root.visit(self.config, self.predictor, numpy.copy(self.board), self.is_first_move))
            loop.run_until_complete(asyncio.gather(*coroutines))

    def predict(self):
        value, visits = self.root.result(self.board.shape[1])
        return value, normalize(visits)

    def visits(self):
        return self.root.result(self.board.shape[1])[1]

    def make_move(self, move):
        self.is_first_move = False
        self.board = make_move(self.board, move)
        if self.root.edges is not None:
            for edge in self.root.edges:
                if edge.node is None:
                    continue
                if edge.move == move:
                    self.root = edge.node
                    return
        self._create_root()

    def _create_root(self):
        values, probabilities = self.model.predict(numpy.array([self.board]))
        size = self.board.shape[1]
        self.root = Node(values[0][0], numpy.reshape(probabilities, (size, size)))

class Node:
    def __init__(self, value, priors):
        self.visits = 1
        self.value = value
        self.priors = priors
        self.edges = None

    async def visit(self, config, predictor, board, is_first_move):
        if self.visits == 1:
            self.is_won = winner(board)
        if self.is_won:
            predictor.release()
            self.visits += 1
            self.value += -1
            return -1
        if self.visits == 1:
            self.edges = []
            size = board.shape[1]
            for x in range(size):
                for y in range(size):
                    if board[0,x,y] == 0 and board[1,x,y] == 0:
                        self.edges.append(Edge(config, self.priors[x,y], (x, y)))
            self.priors = None
        self.visits += 1
        visits_sqrt = math.sqrt(self.visits)
        best_priority, best_edge = -1e9, None
        for edge in self.edges:
            priority = edge.priority(visits_sqrt)
            if priority > best_priority:
                best_priority, best_edge = priority, edge
        value = await best_edge.visit(config, predictor, board, is_first_move)
        self.value += -value
        return -value

    def result(self, size):
        visits = numpy.zeros((size, size))
        for edge in self.edges:
            visits[edge.move[0],edge.move[1]] = edge.node.visits if edge.node else 0
        return self.value / self.visits, visits

class Edge:
    def __init__(self, config, prior, move):
        self.prior = prior
        self.move = move
        self.node = None
        self.uct_priority = config.uct_factor * prior
        self.value_priority = 0.0

    def priority(self, total_visits_sqrt):
        return total_visits_sqrt * self.uct_priority + self.value_priority

    async def visit(self, config, predictor, board, is_first_move):
        if self.node is None:
            self.value_priority = -1e6
            value, priors = await predictor.predict(make_move(board, self.move))
            self.node = Node(value, priors)
        else:
            self.value_priority = -(self.node.value + config.virtual_loss) / (self.node.visits + config.virtual_loss)
            value = await self.node.visit(config, predictor, make_move(board, self.move), False)
        board[0,self.move[0],self.move[1]] = 0
        self.value_priority = -self.node.value / self.node.visits
        # We basically hack this for the swap move. Swap is not implemented, but the search behaves as if it does.
        if is_first_move:
            value = abs(value)
            self.value_priority = -abs(self.value_priority)
        self.uct_priority = config.uct_factor * self.prior / (1 + self.node.visits)
        return value
