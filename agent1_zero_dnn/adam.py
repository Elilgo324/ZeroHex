"""
def update_temp(loss = 1):
    deriev loss according params
    deraive 1-0 loss according temp

    for t in range(num_iterations):
        g = compute_gradient(x,y)
        m = beta_1 * m + (1 - beta_1) * g
        v = beta_2 * v + (1 - beta_2) * np.power(g,2)
        m_hat = m / (1 - np.power(beta_1,t))
        v_hat = v / (1 - np.power(beta_2,t))
        w = w - step_size * m_hat / (np.sqrt(v_hat) + epsilon)

    return 7
"""