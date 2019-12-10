import sys

from keras.layers import Conv2D, Dense, BatchNormalization, Activation, Add, Input, Flatten
from keras.models import Model
from keras.regularizers import l2

from agent1_zero_dnn.config import ModelConfig


def create_model(config, output_file):
    board = Input(shape=(2, config.size, config.size))

    x = Conv2D(config.cnn_filters, config.kernel_size, padding='same', use_bias=False, data_format='channels_first', kernel_regularizer=l2(config.l2_reg))(board)
    x = BatchNormalization(axis=1)(x)
    x = Activation('relu')(x)

    for i in range(config.res_layers):
        start = x
        x = Conv2D(config.cnn_filters, config.kernel_size, padding='same', use_bias=False, data_format='channels_first', kernel_regularizer=l2(config.l2_reg))(x)
        x = BatchNormalization(axis=1)(x)
        x = Activation('relu')(x)
        x = Conv2D(config.cnn_filters, config.kernel_size, padding='same', use_bias=False, data_format='channels_first', kernel_regularizer=l2(config.l2_reg))(x)
        x = BatchNormalization(axis=1)(x)
        x = Add()([x, start])
        x = Activation('relu')(x)
    common = x

    x = Conv2D(1, 1, padding='same', use_bias=False, data_format='channels_first', kernel_regularizer=l2(config.l2_reg))(common)
    x = BatchNormalization(axis=1)(x)
    x = Activation('relu')(x)
    x = Flatten()(x)
    x = Dense(config.value_filters, kernel_regularizer=l2(config.l2_reg))(x)
    x = Activation('relu')(x)
    value = Dense(1, kernel_regularizer=l2(config.l2_reg), activation='tanh')(x)

    x = Conv2D(2, 1, padding='same', use_bias=False, data_format='channels_first', kernel_regularizer=l2(config.l2_reg))(common)
    x = BatchNormalization(axis=1)(x)
    x = Activation('relu')(x)
    x = Flatten()(x)
    policy = Dense(config.size * config.size, kernel_regularizer=l2(config.l2_reg), activation='softmax')(x)

    model = Model(inputs=board, outputs=[value, policy])
    print('%d parameters' % model.count_params(), file=sys.stderr)
    model.save(output_file)


if __name__ == '__main__':
    create_model(ModelConfig(), sys.argv[1])
