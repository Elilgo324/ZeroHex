import numpy as np


def update_temp(loss=1):
    """
    deriev loss according params
    deraive 1-0 loss according temp
    :param loss:
    :return:
    """
    num_iterations = 0
    epsilon = 0
    beta_1 = 0
    beta_2 = 0
    step_size = 0
    m = 0
    v = 0
    w = 0
    x = 0
    y = 0
    for t in range(num_iterations):
        g = compute_gradient(x, y)
        m = beta_1 * m + (1 - beta_1) * g
        v = beta_2 * v + (1 - beta_2) * np.power(g, 2)
        m_hat = m / (1 - np.power(beta_1, t))
        v_hat = v / (1 - np.power(beta_2, t))
        w = w - step_size * m_hat / (np.sqrt(v_hat) + epsilon)

    return None


def compute_gradient(x, y):
    return 0
