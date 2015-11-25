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

# todo: create try except
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from random import randint


class WidgetPlotter:
    """If plots a function on given Widget"""
    def __init__(self, plot_all, plot_3d, plot_meshgrid, main_window):
        # create three figures, canvases and toolbars
        parents = [plot_all, plot_3d, plot_meshgrid]
        self.figures = [plt.figure(figsize=(12, 6), dpi=80, facecolor='w', edgecolor='k') for _ in range(3)]
        self.canvases = [FigureCanvas(figure) for figure in self.figures]
        self.toolbars = [NavigationToolbar(canvas, main_window) for canvas in self.canvases]

        for (parent, canvas, toolbar) in zip(parents, self.canvases, self.toolbars):
            parent.addWidget(toolbar)
            parent.addWidget(canvas)

        self.ax_all_3d = self.figures[0].add_subplot(211, projection='3d')
        self.ax_all_2d = self.figures[0].add_subplot(212)
        self.ax_3d = self.figures[1].add_subplot(111, projection='3d')
        self.ax_2d = self.figures[2].add_subplot(111)

    def plot_example(self):
        self.simple_function()

    def simple_function(self):
        self.ax.hold(False)
        data = [randint(0, 10) for x in range(10)]
        self.ax.plot(data,  range(10))
        self.ax.hold(True)
        self.canvas.draw()

    def plot_function(self, goal_function, drawing_parameters):
        self.clear_axes()
        plt.suptitle("f(x, y) = " + goal_function.get_function_name(), fontsize=14)
        plotter = Plotter(goal_function.get_expression(), *drawing_parameters.get_all_properties())
        plotter.plot_function_in_3d(self.ax_all_3d, self.ax_3d)
        plotter.plot_function_in_color_mesh(self.ax_all_2d, self.ax_2d)
        # todo: create legend
        # plotter.add_legend(self.figure_plot_all)
        for canvas in self.canvases:
            canvas.draw()

    def __hold_axes(self, boolean):
        self.ax_2d.hold(boolean)
        self.ax_3d.hold(boolean)

    def clear_axes(self):
        self.__hold_axes(False)
        self.ax_2d.plot([], [])
        self.ax_3d.plot([], [])
        self.__hold_axes(True)


class Plotter:
    """Plots a function on certain axes"""
    def __init__(self, expression, start=[-1., -1.], stop=[1., 1.], resolution=[0.1, 0.1]):
        self.x_range = np.linspace(start[0], stop[0], (stop[0]-start[0])/resolution[0])
        self.y_range = np.linspace(start[1], stop[1], (stop[1]-start[1]/resolution[1]))

        evaluate = vectorize_expression(expression)
        self.x, self.y = np.meshgrid(self.x_range, self.y_range)
        self.z = evaluate(self.x, self.y)

    def set_x_range_line_space(self, start, stop, num):
        self.x_range = np.linspace(start=start, stop=stop, num=num)

    def set_y_range_line_space(self, start, stop, num):
        self.y_range = np.linspace(start=start, stop=stop, num=num)

    def plot_function_in_3d(self, *axis):
        for axes in axis:
            axes.plot_surface(self.x, self.y, self.z, cmap=cm.jet, rstride=2, cstride=2)
            axes.set_xlabel('x', fontweight='bold')
            axes.set_ylabel('y', fontweight='bold')
            axes.set_zlabel('f(x, y)', fontweight='bold')

            mouse_events = MousePlotEvents()
            mouse_events.zoom(axes)
            mouse_events.reset_3D(axes)

    def plot_function_in_color_mesh(self, *axis):
        for axes in axis:
            self.colormap = axes.pcolormesh(self.x, self.y, self.z, cmap=cm.jet)
            axes.set_xlabel('x', fontweight='bold')
            axes.set_ylabel('y', fontweight='bold')
            axes.yaxis.set_label_position('right')

            mouse_events = MousePlotEvents()
            mouse_events.zoom(axes)
            mouse_events.move(axes)
            mouse_events.reset_2D(axes)

    def add_legend(self, figure):
        figure.subplots_adjust(right=0.8 )
        # self.figure.subplots_adjust(bottom=0.2)
        cbar_ax = figure.add_axes([0.9, 0.1, 0.01, 0.8])
        # cbar_ax = figure.add_axes([0.1, 0.05, 0.8, 0.05])
        figure.colorbar(self.colormap, cax=cbar_ax, orientation='vertical')
        # plt.hold(True)
        # plt.draw()

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
        # TODO: add any number of points -> use np to swap the arrays \
        # you have to join the arrays and split them horizontally into two parts
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




