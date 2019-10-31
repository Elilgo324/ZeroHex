import numpy
import asyncio

class BatchPredictor:
    def __init__(self, model):
        self.model = model
        self.predict_futures = []
        self.predict_boards = []
        self.remaining = 0

    def start_batch(self, batch_size):
        self.remaining = batch_size

    def predict(self, board):
        future = asyncio.Future()
        self.predict_futures.append(future)
        self.predict_boards.append(board)
        self.remaining -= 1
        self._run_if_done()
        return future

    def release(self):
        self.remaining -= 1
        self._run_if_done()

    def _run_if_done(self):
        if self.remaining < 0:
            raise Exception('PredictBatch already done')
        if self.remaining > 0 or not self.predict_futures:
            return
        size = self.predict_boards[0].shape[1]
        values, priors = self.model.predict(numpy.array(self.predict_boards))
        for i in range(len(self.predict_futures)):
            self.predict_futures[i].set_result((values[i][0], numpy.reshape(priors[i], (size, size))))
        self.predict_futures = []
        self.predict_boards = []
