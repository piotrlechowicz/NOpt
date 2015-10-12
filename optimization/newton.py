__author__ = 'piotr'

import numpy as np
from optimization_tools import GradientAlgorithm


class NewtonAlgorithm(GradientAlgorithm):
    def __init__(self, expression, start, stop, num_of_values, tolerance=0.1, tau=1):
        GradientAlgorithm.__init__(self, expression, start, stop, num_of_values)
        self.tolerance = tolerance
        self.tau = tau


if __name__ == "__main__":
    from py_expression_eval import Parser
    import numpy as np
    parser = Parser()
    expr = parser.parse('x^2 + y^3')
    na = NewtonAlgorithm(expr, [-2., -2.], [2., 2.], [101, 101])
    y = x = np.linspace(-2., 2., 101)
    mx, my = np.meshgrid(x, y)
    eval = np.vectorize(lambda x, y: expr.evaluate({'x': x, 'y': y}))
    z1 = eval(mx, my)
    print na.value_at(-2., -2.)
    print z1[0][0], na.z[0][0]
