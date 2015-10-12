import sys

from optimization.optimization_tools import vectorize_expression

try:
    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib import cm
    import matplotlib.pyplot as plt
    import numpy as np
except ImportError as error:
    print error.message
    sys.exit("Not all the requirements are fulfilled")


from events import MousePlotEvents


class Plotter:
    """Plots a function"""
    def __init__(self):
        self.x_range = np.linspace(-1., 1., 100)
        self.y_range = np.linspace(-1., 1., 100)

    def set_x_range_linspace(self, start, stop, num):
        self.x_range = np.linspace(start=start, stop=stop, num=num)
    
    def set_y_range_linspace(self, start, stop, num):
        self.y_range = np.linspace(start=start, stop=stop, num=num)

    def plot(self, expression, function_name):
        evaluate = vectorize_expression(expression)
        x, y = np.meshgrid(self.x_range, self.y_range)
        z = evaluate(x, y)

        fig = plt.figure(figsize=(12, 6), dpi=80, facecolor='w', edgecolor='k')
        plt.suptitle("f(x, y) = " + function_name, fontsize=14)

        # left surface plot
        ax = fig.add_subplot(121, projection='3d')
        ax.plot_surface(x, y, z, cmap=cm.jet, rstride=2, cstride=2)
        ax.set_xlabel('x', fontweight='bold')
        ax.set_ylabel('y', fontweight='bold')
        ax.set_zlabel('f(x, y)', fontweight='bold')

        mouse_events = MousePlotEvents()
        mouse_events.zoom(ax)
        mouse_events.reset_3D(ax)

        ax2 = fig.add_subplot(122)
        im = ax2.pcolormesh(x, y, z, cmap=cm.jet)
        ax2.set_xlabel('x', fontweight='bold')
        ax2.set_ylabel('y', fontweight='bold')
        ax2.yaxis.set_label_position('right')
        # ax.yaxis.tick_right()

        mouse_events2 = MousePlotEvents()
        mouse_events2.zoom(ax2)
        mouse_events2.move(ax2)
        mouse_events2.reset_2D(ax2)

        fig.subplots_adjust(bottom=0.2)
        cbar_ax = fig.add_axes([0.1, 0.05, 0.8, 0.05])
        fig.colorbar(im, cax=cbar_ax, orientation='horizontal')

        plt.show()


def test_plot():
    from py_expression_eval import Parser
    parser = Parser()
    expr = parser.parse('x^2 + y^2')
    plotter = Plotter()
    plotter.plot(expr, expr.toString())


if __name__ == "__main__":
    test_plot()




