class ModelConfig:
    def __init__(self, size=11, kernel_size=3, l2_reg=1e-4, res_layers=6, cnn_filters=16, value_filters=16):
        self.size = size
        self.kernel_size = kernel_size
        self.l2_reg = l2_reg
        self.res_layers = res_layers
        self.cnn_filters = cnn_filters
        self.value_filters = value_filters


class SearchConfig:
    def __init__(self, batch_size=16, virtual_loss=3, uct_factor=5.0):
        self.batch_size = batch_size
        self.virtual_loss = virtual_loss
        self.uct_factor = uct_factor


class TrainConfig:
    def __init__(self, size=11, batch_size=32, learning_rate=1e-2, momentum=0.9, epochs=100, history_size=100000, validation_ratio=10):
        self.size = size
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.momentum = momentum
        self.epochs = epochs
        self.history_size = history_size
        self.validation_ratio = validation_ratio


class GenerateConfig:
    def __init__(self, size=11, batch_size=32, iterations=20, search_config=None):
        self.size = size
        self.batch_size = batch_size
        self.iterations = iterations
        self.search_config = SearchConfig() if search_config is None else search_config


class GtpConfig:
    def __init__(self, size=11, iterations=200, search_config=None):
        self.size = size
        self.iterations = iterations
        self.search_config = SearchConfig() if search_config is None else search_config


class CompareConfig:
    def __init__(self, size=11, iterations=20, search_config=None):
        self.size = size
        self.iterations = iterations
        self.search_config = SearchConfig() if search_config is None else search_config
