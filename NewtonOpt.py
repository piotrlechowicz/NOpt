__author__ = 'Piotr Lechowicz'

import sys

try:
    from py_expression_eval import Parser
except ImportError as error:
    print error.message
    print "py_expression_eval is necessary"
    sys.exit("Not all the requirements are fulfilled")

try:
    from PyQt5.QtWidgets import QApplication, QMainWindow
except ImportError as error:
    print error.message
    print "PyQt5 is necessary"
    sys.exit("Not all the requirements are fulfilled")

from expression.goal_function import GoalFunction
from expression.validate import ExpressionValidator
from plot.plot import Plotter
from optimization.newton import NewtonAlgorithm
from numpy import array
from qtgui import gui

# Interesting function: (x+1)^2 * (y-1)^4 + (y+1)^4 * (x-1)^2

import matplotlib
# matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt


class App(QMainWindow, gui.Ui_MainWindow):
    def __init__(self, parent=None):
        super(App, self).__init__(parent)
        self.setupUi(self)

        # define connections
        self.executeButton.clicked.connect(self.executeButtonClicked)

    def executeButtonClicked(self):
        print "exec clicked"

    def run(self):
        # main program loop
        while True:
            print "Enter a goal function"
            user_input = raw_input()
            if user_input == "quit":
                break

            # application logic
            goal_function = GoalFunction()
            parser = Parser()
            try:
                goal_function.expression = parser.parse(user_input)
                goal_function.fetch_function_name()
            except Exception as exception:
                print exception.message
                continue

            expression_validator = ExpressionValidator(goal_function.expression, goal_function.variables)
            goal_function.expression, validates, validation_error = expression_validator.validate()

            if not validates:
                print validation_error
                continue

            print goal_function.expression.toString()

            # TODO: add validation of parameters
            # TODO: create more user friend api
            # TODO: to many numpy calculations
            # get drawing parameters
            parameters_calculations = self.get_function_range_parameters()
            parameters_drawing = parameters_calculations

            parameters_drawing[2][0] /= 10
            parameters_drawing[2][1] /= 10

            # plot function
            print goal_function.function_name
            plotter = Plotter(goal_function.expression, goal_function.function_name, *parameters_drawing)
            plotter.plot_function_in_3D()

            # add plot on the gui
            figure = plt.figure()
            canvas = FigureCanvas(figure)
            toolbar = NavigationToolbar(canvas, self)
            self.matPlotLayout.addWidget(toolbar)
            self.matPlotLayout.addWidget(canvas)
            data = [range(10)]
            ax = figure.add_subplot(111)
            ax.hold(True)
            ax.plot(data)
            canvas.draw()


            na = NewtonAlgorithm(goal_function.expression, *parameters_calculations, debug=True)
            # starting point
            xn = array([[3.], [3.5]])
            na.set_starting_point_numpy_array(xn)
            min_found = False
            while not min_found:
                xnn, min_found = na.next_step()
                plotter.add_to_result_numpy_points(xn, xnn)
                xn = xnn

            plotter.wait_to_close_plot_windows()

    def get_function_range_parameters(self):
        print "enter: start, stop, num_od_values"
        user_input = raw_input()
        user_input = user_input.split(',')
        parameters = []
        if user_input.__len__() >= 3:
            for par in input:
                par = float(par)
                parameters.append([par, par])
        else:
            parameters.extend([[-4., -4.], [4., 4.], [1000, 1000]])
        return parameters


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = App()
    form.show()
    form.run()
    app.exec_()
