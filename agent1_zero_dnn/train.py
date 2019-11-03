import os
import numpy
import sys

from keras.models import load_model
from keras.optimizers import SGD
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.utils import Sequence

from serialize import read_record, record_size
from game import normalize, symmetry, symmetry_probs
from config import TrainConfig


class GameData(Sequence):
    def __init__(self, config, path, is_validation):
        self.record_size = record_size(config.size)
        self.config = config
        self.path = path
        self.is_validation = is_validation
        self.file = open(self.path, 'rb')
        self.on_epoch_end()

    def __len__(self):
        return self.batch_count

    def __getitem__(self, idx):
        parity = idx & 1
        idx >>= 1
        if self.is_validation:
            idx = self.config.validation_ratio * (idx + 1) - 1
        else:
            idx = self.config.validation_ratio * idx // (self.config.validation_ratio - 1)
        self.file.seek(self.record_offset * self.record_size + idx * self.record_size * self.config.batch_size)
        batch_board = []
        batch_value = []
        batch_probs = []
        for i in range(self.config.batch_size):
            board, won, visits = read_record(self.file, self.config.size)
            batch_value.append(1.0 if won else -1.0)
            if numpy.sum(visits, (0, 1)) == 0:
                print(visits, file=sys.stderr)
                raise Exception('Invalid example')
            probs = normalize(visits)
            if parity == i & 1:
                board = symmetry(board)
                probs = symmetry_probs(probs)
            batch_board.append(board)
            batch_probs.append(numpy.reshape(probs, self.config.size * self.config.size))
        return numpy.array(batch_board), [numpy.array(batch_value), numpy.array(batch_probs)]

    def on_epoch_end(self):
        record_count = os.path.getsize(self.path) // self.record_size
        self.record_offset = max(0, record_count - self.config.history_size)
        record_count -= self.record_offset
        raw_batch_count = record_count // self.config.batch_size
        if self.is_validation:
            self.batch_count = raw_batch_count // self.config.validation_ratio
        else:
            self.batch_count = raw_batch_count - raw_batch_count // self.config.validation_ratio
        self.batch_count *= 2


def train(config, model_file, data_file):
    model = load_model(model_file)
    model.compile(
        optimizer=SGD(lr=config.learning_rate, momentum=config.momentum),
        loss=['mse', 'categorical_crossentropy'],
        loss_weights=[1., 1.],
    )

    training_seq = GameData(config, data_file, False)
    validation_seq = GameData(config, data_file, True)

    model.fit_generator(
        training_seq,
        epochs=config.epochs,
        steps_per_epoch=len(training_seq),
        validation_data=validation_seq,
        validation_steps=len(validation_seq),
        callbacks=[
            ModelCheckpoint(model_file, save_best_only=True),
            EarlyStopping(patience=5),
        ],
    )


if __name__ == '__main__':
    train(TrainConfig(), sys.argv[1], sys.argv[2])
