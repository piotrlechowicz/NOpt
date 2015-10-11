__author__ = 'piotr'

import numpy as np
from function_tools import GradientAlgorithm


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



    # import numpy as np
    # import numdifftools as nd
    # from scipy.optimize import minimize
    # from sympy import *
    #
    # def fun(x, y):
    #     return x ** 2 + y ** 3
    #
    # x = np.linspace(-1., 1., 101)
    # y = np.linspace(-1., 1., 101)
    #
    # print x[75], y[75]
    #
    # dy = dx = 2. / 101
    #
    # fun = np.vectorize(fun)
    #
    # x, y = np.meshgrid(x, y)
    #
    # z = fun(x, y)
    #
    # print z[75][75]
    #
    # gy, gx = np.gradient(z, dx, dy)
    #
    #
    #
    # print gx[75][75], gy[75][75]
    #
    # gxy, gxx = np.gradient(gx, dx, dy)
    # gyy, gyx = np.gradient(gy, dx, dy)
    #
    # print y[98][98]
    # print gxx[75][75], gxy[75][75], gyx[75][75], gyy[75][75]
    # print gxx[98][98], gxy[100][100], gyx[100][100], gyy[98][98]
