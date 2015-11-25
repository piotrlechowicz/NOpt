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
from plot.plot import Plotter, WidgetPlotter
from optimization.newton import NewtonAlgorithm
from numpy import array
from qtgui import gui

from application.ApplicationProperties import NewtonAlgorithmProperties, DrawingProperties

# Interesting function: (x+1)^2 * (y-1)^4 + (y+1)^4 * (x-1)^2

from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt


class App(QMainWindow, gui.Ui_MainWindow):
    """Main class which controls the flow of an application"""
    def __init__(self, parent=None):
        super(App, self).__init__(parent)
        self.setupUi(self)                                          # create gui components
        self.goal_function = GoalFunction()                         # goal function of an algorithm
        self.newton_properties = NewtonAlgorithmProperties()        # create properties holder
        self.drawing_properties = DrawingProperties()               # drawing properties holder
        self.__set_fields_logic()                                   # connect gui fields to the logic of an application
        self.update_fields()                                        # get values of all fields

    def __set_fields_logic(self):
        """Set connection between fields and its logic"""
        self.executeButton.clicked.connect(self.execute_button_clicked)
        self.formulaInput.returnPressed.connect(self.formula_inserted)
        self.npStartingPointX.textChanged.connect(self.set_np_starting_point)
        self.npStartingPointY.textChanged.connect(self.set_np_starting_point)
        self.npStartBoundaryX.textChanged.connect(self.set_np_start_boundary)
        self.npStartBoundaryY.textChanged.connect(self.set_np_start_boundary)
        self.npStopBoundaryX.textChanged.connect(self.set_np_stop_boundary)
        self.npStopBoundaryY.textChanged.connect(self.set_np_stop_boundary)
        self.npResolutionX.textChanged.connect(self.set_np_resolution)
        self.npResolutionY.textChanged.connect(self.set_np_resolution)
        self.npTolerance.textChanged.connect(self.set_np_tolerance)
        self.dpStartBoundaryX.textChanged.connect(self.set_dp_start_boundary)
        self.dpStartBoundaryY.textChanged.connect(self.set_dp_start_boundary)
        self.dpStopBoundaryX.textChanged.connect(self.set_dp_stop_boundary)
        self.dpStopBoundaryY.textChanged.connect(self.set_dp_stop_boundary)
        self.dpResolutionX.textChanged.connect(self.set_dp_resolution)
        self.dpResolutionY.textChanged.connect(self.set_dp_resolution)

    def update_fields(self):
        """Update values of all fields"""
        self.formulaInput.setText(self.goal_function.get_function_name())
        np = self.newton_properties.get_all_properties()
        dp = self.drawing_properties.get_all_properties()
        self.npStartingPointX.setText(str(np[0][0]))
        self.npStartingPointY.setText(str(np[0][1]))
        self.npStartBoundaryX.setText(str(np[1][0]))
        self.npStartBoundaryY.setText(str(np[1][1]))
        self.npStopBoundaryX.setText(str(np[2][0]))
        self.npStopBoundaryY.setText(str(np[2][1]))
        self.npResolutionX.setText(str(np[3][0]))
        self.npResolutionY.setText(str(np[3][1]))
        self.npTolerance.setText(str(np[4]))
        self.dpStartBoundaryX.setText(str(dp[0][0]))
        self.dpStartBoundaryY.setText(str(dp[0][1]))
        self.dpStopBoundaryX.setText(str(dp[1][0]))
        self.dpStopBoundaryY.setText(str(dp[1][1]))
        self.dpResolutionX.setText(str(dp[2][0]))
        self.dpResolutionY.setText(str(dp[2][1]))

    def execute_button_clicked(self):
        self.run()

    def set_np_starting_point(self):
        self.__text_filed_caller(self.newton_properties.set_starting_point,
                                 self.npStartingPointX,
                                 self.npStartingPointY)

    def set_np_start_boundary(self):
        self.__text_filed_caller(self.newton_properties.set_start_boundary,
                                 self.npStartBoundaryX,
                                 self.npStartBoundaryY)

    def set_np_stop_boundary(self):
        self.__text_filed_caller(self.newton_properties.set_stop_boundary,
                                 self.npStopBoundaryX,
                                 self.npStopBoundaryY)

    def set_np_resolution(self):
        self.__text_filed_caller(self.newton_properties.set_resolution,
                                 self.npResolutionX,
                                 self.npResolutionY)

    def set_np_tolerance(self):
        self.__text_filed_caller(self.newton_properties.set_tolerance,
                                 self.npTolerance)

    def set_dp_start_boundary(self):
        self.__text_filed_caller(self.drawing_properties.set_start_boundary,
                                 self.dpStartBoundaryX,
                                 self.dpStartBoundaryY)

    def set_dp_stop_boundary(self):
        self.__text_filed_caller(self.drawing_properties.set_stop_boundary,
                                 self.dpStopBoundaryX,
                                 self.dpStopBoundaryY)

    def set_dp_resolution(self):
        self.__text_filed_caller(self.drawing_properties.set_resolution,
                                 self.dpResolutionX,
                                 self.dpResolutionY)

    def formula_inserted(self):
        self.__text_filed_caller(self.goal_function.set_goal_function,
                                 self.formulaInput)

    @staticmethod
    def __text_filed_caller(function, *fields):
        """function used to holding errors from getting values of text fields
        It colours incorrect output with red and disable the possibility
        of calling algorithm when error occurred.
        """
        params = []
        for field in fields:
            params.append(field.text())
        if function(*params):
            for field in fields:
                field.setStyleSheet("background-color: white")
        else:
            for field in fields:
                field.setStyleSheet("background-color: #aa0000")

    def run(self):
        if not self.goal_function.is_correctly_parsed():        # if function not parsed, return
            return

        plotter = WidgetPlotter(self.matPlotLayout)
        # todo: move it to plotter
            # add plot on the gui
        # figure = plt.figure()
        # canvas = FigureCanvas(figure)
        # toolbar = NavigationToolbar(canvas, self)
        # self.matPlotLayout.addWidget(toolbar)
        # self.matPlotLayout.addWidget(canvas)
        # data = [range(10)]
        # ax = figure.add_subplot(111)
        # ax.hold(True)
        # ax.plot(data)
        # canvas.draw()

        # plot function
        # while True:

        #
        #     # TODO: add validation of parameters
        #     # TODO: create more user friend api
        #     # TODO: to many numpy calculations
        #     # get drawing parameters
        #     parameters_calculations = self.get_function_range_parameters()
        #     parameters_drawing = parameters_calculations
        #
        #     parameters_drawing[2][0] /= 10
        #     parameters_drawing[2][1] /= 10
        #
        #     # plot function
        #     print goal_function.function_name
        #     plotter = Plotter(goal_function.expression, goal_function.function_name, *parameters_drawing)
        #     plotter.plot_function_in_3D()
        #
        #     # todo: move it to plotter
        #     # add plot on the gui
        #     figure = plt.figure()
        #     canvas = FigureCanvas(figure)
        #     toolbar = NavigationToolbar(canvas, self)
        #     self.matPlotLayout.addWidget(toolbar)
        #     self.matPlotLayout.addWidget(canvas)
        #     data = [range(10)]
        #     ax = figure.add_subplot(111)
        #     ax.hold(True)
        #     ax.plot(data)
        #     canvas.draw()
        #
        #
        #     na = NewtonAlgorithm(goal_function.expression, *parameters_calculations, debug=True)
        #     # starting point
        #     xn = array([[3.], [3.5]])
        #     na.set_starting_point_numpy_array(xn)
        #     min_found = False
        #     while not min_found:
        #         xnn, min_found = na.next_step()
        #         plotter.add_to_result_numpy_points(xn, xnn)
        #         xn = xnn
        #
        #     plotter.wait_to_close_plot_windows()

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

    app.exec_()
    form.run()
