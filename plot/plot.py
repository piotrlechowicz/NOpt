import sys

from optimization.optimization_tools import vectorize_expression

try:
    import matplotlib
    version = matplotlib.__version__.split(',')
    if version < [1, 5, 0]:
        print "matplotlib has to be in version 1.5.0 or greater"
        sys.exit(1)
    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib import cm
    from matplotlib.backends.backend_qt5agg import FigureCanvas
    from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
    import matplotlib.pyplot as plt
    import numpy as np
except ImportError as error:
    print error.message
    sys.exit("Not all the requirements are fulfilled")

from events import MousePlotEvents


class WidgetPlotter:
    """It plots a function on given Widget"""
    def __init__(self, plot_all, plot_3d, plot_meshgrid, main_window):
        """Creates three figures, canvases and toolbars
        For figure with 3d image and mesh grid,
        figure with 3d image,
        figure with mesh grid.
        It initialize figures with subplots.
        """
        parents = [plot_all, plot_3d, plot_meshgrid]
        self.figures = [plt.figure(figsize=(12, 6), dpi=80, facecolor='w', edgecolor='k') for _ in range(3)]
        self.canvases = [FigureCanvas(figure) for figure in self.figures]
        self.toolbars = [NavigationToolbar(canvas, main_window) for canvas in self.canvases]

        for (parent, canvas, toolbar) in zip(parents, self.canvases, self.toolbars):
            parent.addWidget(toolbar)
            parent.addWidget(canvas)

        self.axis_all_3d = self.figures[0].add_subplot(211, projection='3d')
        self.axis_all_2d = self.figures[0].add_subplot(212)
        self.axis_3d = self.figures[1].add_subplot(111, projection='3d')
        self.axis_2d = self.figures[2].add_subplot(111)
        self.axes = [self.axis_all_2d, self.axis_all_3d, self.axis_2d, self.axis_3d]

    def plot_function(self, goal_function, drawing_parameters):
        """Plots function based on the goal function
        and parameters of drawing
        """
        self.clear_axes()
        plt.suptitle("f(x, y) = " + goal_function.get_function_name(), fontsize=14)
        plotter = Plotter(goal_function.get_expression(), *drawing_parameters.get_all_properties())
        plotter.plot_function_in_3d(self.axis_all_3d, self.axis_3d)
        plotter.plot_function_in_color_mesh(self.axis_all_2d, self.axis_2d)
        plotter.add_legends(*self.figures)
        for canvas in self.canvases:
            canvas.draw()

    def add_values_to_mesh_grid(self, **values):
        """draw line(s) on a mesh grid
        As an argument it takes a dictionary
        where the keys are 'x' and 'y'
        and values are arrays with points
        """
        x_array = values.get('x', [])
        y_array = values.get('y', [])
        Plotter.add_points_to_axes(x_array, y_array, self.axis_2d, self.axis_all_2d)
        for canvas in self.canvases:
            canvas.draw()

    def add_numpy_points_to_mesh_grid(self, *numpy_points):
        """add list of numpy points to mesh grid"""
        axes = {"1": self.axis_2d,
                "2": self.axis_all_2d}
        Plotter.add_numpy_points_to_axes(*numpy_points, **axes)
        for canvas in self.canvases:
            canvas.draw()

    def __hold_axes(self, boolean):
        """Determine whether axes are held"""
        for axis in self.axes:
            axis.hold(boolean)

    def clear_axes(self):
        """Clear content of axes"""
        self.__hold_axes(False)
        for axis in self.axes:
            axis.plot([], [])
        self.__hold_axes(True)


class Plotter:
    """Plots a function on certain axis"""
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

    def plot_function_in_3d(self, *axes):
        """Plot 3d function on given axes"""
        for axis in axes:
            axis.plot_surface(self.x, self.y, self.z, cmap=cm.jet, rstride=2, cstride=2)
            axis.set_xlabel('x', fontweight='bold')
            axis.set_ylabel('y', fontweight='bold')
            axis.set_zlabel('f(x, y)', fontweight='bold')

            mouse_events = MousePlotEvents()
            mouse_events.zoom(axis)
            mouse_events.reset_3D(axis)

    def plot_function_in_color_mesh(self, *axes):
        """Plot mesh grid on given axes"""
        for axis in axes:
            self.colormap = axis.pcolormesh(self.x, self.y, self.z, cmap=cm.jet)
            axis.set_xlabel('x', fontweight='bold')
            axis.set_ylabel('y', fontweight='bold')
            axis.yaxis.set_label_position('right')

            mouse_events = MousePlotEvents()
            mouse_events.zoom(axis)
            mouse_events.move(axis)
            mouse_events.reset_2D(axis)

    def add_legends(self, *figures):
        """add colormap legend to figures"""
        for figure in figures:
            figure.subplots_adjust(right=0.8)
            cbar_ax = figure.add_axes([0.9, 0.1, 0.01, 0.8])
            figure.colorbar(self.colormap, cax=cbar_ax, orientation='vertical')

    @staticmethod
    def add_points_to_axes(x_values, y_values, *axes):
        """adds to axes lists of x and y values"""
        for axis in axes:
            axis.plot(x_values, y_values, 'mo:')

    @staticmethod
    def add_numpy_points_to_axes(*points, **axes):
        """Points are passed as a list
        axes as a dictionary -> axes are values
        """
        x_array = []
        y_array = []
        for point in points:
            x_array.append(point[0][0])
            y_array.append(point[1][0])
        for axis in axes.values():
            axis.plot(x_array, y_array, 'mo:')

    @staticmethod
    def wait_to_close_plot_windows():
        plt.show()


def test_plot():
    from py_expression_eval import Parser
    parser = Parser()
    expr = parser.parse('x^2 + y^2')
    plotter = Plotter(expr, expr.toString())
    plotter.plot_function_in_3D()


if __name__ == "__main__":
    test_plot()




