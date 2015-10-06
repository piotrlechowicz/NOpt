from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np
from py_expression_eval import Parser


def main():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    parser = Parser()
    expr = parser.parse('x^2 + y^2')

    x_range = np.linspace(-2., 2., 100)
    y_range = np.linspace(-2., 2., 100)

    X, Y = np.meshgrid(x_range, y_range)

    def eval(x, y):
        return expr.evaluate({'x': x, 'y': y})

    fun = np.vectorize(eval)

    z = fun(x_range, y_range)

    ax.plot_surface(X, Y, z, rstride=1, cstride=1, cmap=cm.jet,
                    linewidth=0, antialiased=False)

    plt.show()

if __name__ == "__main__":
    main()
