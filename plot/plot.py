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
    def __init__(self, expression, function_name, start=[-1., -1.], stop=[1., 1.], num_of_val=[101, 101]):
        self.x_range = np.linspace(start[0], stop[0], num_of_val[0])
        self.y_range = np.linspace(start[1], stop[1], num_of_val[1])

        self.function_name = function_name
        evaluate = vectorize_expression(expression)
        self.x, self.y = np.meshgrid(self.x_range, self.y_range)
        self.z = evaluate(self.x, self.y)

        self.res_ax = None

    def set_x_range_linspace(self, start, stop, num):
        self.x_range = np.linspace(start=start, stop=stop, num=num)

    def set_y_range_linspace(self, start, stop, num):
        self.y_range = np.linspace(start=start, stop=stop, num=num)

    def plot_function_in_3D(self):
        fig = plt.figure(figsize=(12, 6), dpi=80, facecolor='w', edgecolor='k')
        plt.suptitle("f(x, y) = " + self.function_name, fontsize=14)

        # left surface plot
        ax = fig.add_subplot(121, projection='3d')
        ax.plot_surface(self.x, self.y, self.z, cmap=cm.jet, rstride=2, cstride=2)
        ax.set_xlabel('x', fontweight='bold')
        ax.set_ylabel('y', fontweight='bold')
        ax.set_zlabel('f(x, y)', fontweight='bold')

        mouse_events = MousePlotEvents()
        mouse_events.zoom(ax)
        mouse_events.reset_3D(ax)

        self.res_ax = fig.add_subplot(122)
        im = self.res_ax.pcolormesh(self.x, self.y, self.z, cmap=cm.jet)
        self.res_ax.set_xlabel('x', fontweight='bold')
        self.res_ax.set_ylabel('y', fontweight='bold')
        self.res_ax.yaxis.set_label_position('right')
        # ax.yaxis.tick_right()

        mouse_events2 = MousePlotEvents()
        mouse_events2.zoom(self.res_ax)
        mouse_events2.move(self.res_ax)
        mouse_events2.reset_2D(self.res_ax)

        fig.subplots_adjust(bottom=0.2)
        cbar_ax = fig.add_axes([0.1, 0.05, 0.8, 0.05])
        fig.colorbar(im, cax=cbar_ax, orientation='horizontal')

        plt.hold(True)
        plt.draw()

    # def plot_result(self):
    #     fig = plt.figure(figsize=(6, 6), dpi=80, facecolor='w', edgecolor='k')
    #     plt.suptitle("f(x, y) = " + self.function_name, fontsize=14)
    #
    #     self.res_ax = fig.add_subplot(111)
    #     im = self.res_ax.pcolormesh(self.x, self.y, self.z, cmap=cm.jet)
    #     self.res_ax.set_xlabel('x', fontweight='bold')
    #     self.res_ax.set_ylabel('y', fontweight='bold')
    #     self.res_ax.yaxis.set_label_position('right')
    #
    #     mouse_events = MousePlotEvents()
    #     mouse_events.zoom(self.res_ax)
    #     mouse_events.move(self.res_ax)
    #     mouse_events.reset_2D(self.res_ax)
    #
    #     fig.subplots_adjust(bottom=0.2)
    #     cbar_ax = fig.add_axes([0.1, 0.05, 0.8, 0.05])
    #     fig.colorbar(im, cax=cbar_ax, orientation='horizontal')
    #
    #     plt.hold(True)

    def add_to_result(self, x, y):
        self.res_ax.plot(x, y, 'mo:')
        plt.draw()

    def add_to_result_numpy_points(self, fst_point, snd_point):
        self.res_ax.plot([fst_point[0][0], snd_point[0][0]], [fst_point[1][0], snd_point[1][0]], 'mo:')
        # TODO: add any number of points -> use np to swap the arrays
        plt.draw()

    def wait_to_close_plot_windows(self):
        plt.show()


def test_plot():
    from py_expression_eval import Parser
    parser = Parser()
    expr = parser.parse('x^2 + y^2')
    plotter = Plotter(expr, expr.toString())
    plotter.plot_function_in_3D()


if __name__ == "__main__":
    test_plot()




