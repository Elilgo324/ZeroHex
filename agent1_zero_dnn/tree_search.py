import math
import random

import numpy
import asyncio

from game import winner, make_move, normalize
from batch_predictor import BatchPredictor

import numpy as np

"""
MCTS algo

Selection: In this process, the MCTS algorithm traverses the current 
tree from the root node using a specific strategy.
The strategy uses an evaluation function to optimally select nodes
with the highest estimated value. MCTS uses the Upper Confidence Bound
(UCB) formula applied to trees as the strategy in the selection 
process to traverse the tree. It balances the exploration-exploitation
trade-off. During tree traversal, a node is selected based on some
parameters that return the maximum value. The parameters are 
characterized by the formula that is typically used for this purpose 
is given below.

wi / n1 + c * sqrt( ln(Ni) / ni )

wi = num of wins for the node after the i-th move
ni = num of simulations for the node after the i-th move
Ni = total num of simulations ran by the parent node
C = exploration parameter

When traversing a tree during the selection process, the child node
that returns the greatest value from the above equation will be one
that will get selected. During traversal, once a child node is found
which is also a leaf node, the MCTS jumps into the expansion step.
Expansion: In this process, a new child node is added to the tree to
that node which was optimally reached during the selection process.
Simulation: In this process, a simulation is performed by choosing
moves or strategies until a result or predefined state is achieved.
Backpropagation: After determining the value of the newly added node,
the remaining tree must be updated. So, the backpropagation process
is performed, where it backpropagates from the new node to the root
node. During the process, the number of simulation stored in each node
is incremented. Also, if the new node’s simulation results in a win,
then the number of wins is also incremented.
"""

def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()

def temperature(probs, t):
    probs = np.array(probs)
    probs = np.power(probs, 1/t) / np.sum(np.power(probs, 1/t))
    return probs


class TreeSearchPredictor:
    def __init__(self, config, model, board, is_first_move, t=1, T=1):
        self.t = t
        self.T = T
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
        return value, temperature(normalize(visits),self.T)

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
        #self.edges = None
        self.edges = []
        self.t = 1

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

        """
        insert temperature here
        """
        priorities = [edge.priority(visits_sqrt) for edge in self.edges]
        probabilities = softmax(priorities)
        temp_probabilities = temperature(probabilities, self.t)

        shlomo_probs = [(x+(random.randint(0,3)/10000)) for x in temp_probabilities]

        best_edge_index = np.argmax(shlomo_probs)
        best_edge = self.edges[best_edge_index]

        value = await best_edge.visit(config, predictor, board, is_first_move)
        self.value += -value
        return -value

    def result(self, size):
        visits = numpy.zeros((size, size))
        for edge in self.edges:
            visits[edge.move[0], edge.move[1]] = edge.node.visits if edge.node else 0
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
            # dg of value_priority
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
