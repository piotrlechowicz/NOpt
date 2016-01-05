import sys

try:
    from PyQt5.QtWidgets import QApplication, QMainWindow
except ImportError as error:
    print error.message
    print "PyQt5 is necessary"
    sys.exit("Not all the requirements are fulfilled")

from expression.goal_function import GoalFunction
from plot.plot import WidgetPlotter
from optimization.newton import NewtonAlgorithm
from qtgui import gui

from application.application_properties import NewtonAlgorithmProperties, DrawingProperties
from logger.logger import ConsoleLogger, ResultLogger, LoggerLevel
from utils.numpy_utils import convert_array_to_numpy_point
from application.function_chooser import PredefinedFunctions


class App(QMainWindow, gui.Ui_MainWindow):
    """Main class which controls the flow of an application"""
    def __init__(self, parent=None):
        super(App, self).__init__(parent)
        self.setupUi(self)                                          # create gui components
        self.__custom_init_settings()
        self.application_logic = ApplicationLogic(self)
        self.newton_properties = NewtonAlgorithmProperties()        # create properties holder
        self.drawing_properties = DrawingProperties()               # drawing properties holder
        self.__set_text_fields_logic()                              # connect gui fields to the logic of an application
        self.__set_buttons_logic()
        self.update_fields()                                        # get values of all fields
        self.plotter = WidgetPlotter(self.plotAllLayout,
                                     self.plot3dLayout,
                                     self.plotMeshgridLayout,
                                     self)                          # plotter to plot the results

    def __custom_init_settings(self):
        """Set up some UI components"""
        self.npWidget.setVisible(False)
        self.dpWidget.setVisible(False)

    def __set_buttons_logic(self):
        self.executeButton.clicked.connect(self.execute_button_clicked)
        self.npToolButton.clicked.connect(lambda: self.application_logic.toggle_visibility(
            self.npWidget
        ))
        self.dpToolButton.clicked.connect(lambda: self.application_logic.toggle_visibility(
            self.dpWidget
        ))
        self.drawButton.clicked.connect(self.draw_button_clicked)
        self.chooseFunctionComboBox.currentTextChanged.connect(self.application_logic.predefined_function_selected)

    def execute_button_clicked(self):
        self.application_logic.run()

    def draw_button_clicked(self):
        self.application_logic.draw()

    def __set_text_fields_logic(self):
        """Set connection between fields and its logic"""
        self.formulaInput.returnPressed.connect(self.application_logic.formula_inserted)
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
        self.formulaInput.setText(self.application_logic.goal_function.get_function_name())
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

    def update_newton_properties_fields(self):
        np = self.newton_properties.get_all_properties()
        self.npStartingPointX.setText(str(np[0][0]))
        self.npStartingPointY.setText(str(np[0][1]))
        self.npStartBoundaryX.setText(str(np[1][0]))
        self.npStartBoundaryY.setText(str(np[1][1]))
        self.npStopBoundaryX.setText(str(np[2][0]))
        self.npStopBoundaryY.setText(str(np[2][1]))
        self.npResolutionX.setText(str(np[3][0]))
        self.npResolutionY.setText(str(np[3][1]))
        self.npTolerance.setText(str(np[4]))

    def set_np_starting_point(self):
        self.application_logic.text_field_caller(self.newton_properties.set_starting_point,
                                                 self.npStartingPointX,
                                                 self.npStartingPointY)

    def set_np_start_boundary(self):
        self.application_logic.text_field_caller(self.newton_properties.set_start_boundary,
                                                 self.npStartBoundaryX,
                                                 self.npStartBoundaryY)

    def set_np_stop_boundary(self):
        self.application_logic.text_field_caller(self.newton_properties.set_stop_boundary,
                                                 self.npStopBoundaryX,
                                                 self.npStopBoundaryY)

    def set_np_resolution(self):
        self.application_logic.text_field_caller(self.newton_properties.set_resolution,
                                                 self.npResolutionX,
                                                 self.npResolutionY)

    def set_np_tolerance(self):
        self.application_logic.text_field_caller(self.newton_properties.set_tolerance,
                                                 self.npTolerance)

    def set_dp_start_boundary(self):
        self.application_logic.text_field_caller(self.drawing_properties.set_start_boundary,
                                                 self.dpStartBoundaryX,
                                                 self.dpStartBoundaryY)

    def set_dp_stop_boundary(self):
        self.application_logic.text_field_caller(self.drawing_properties.set_stop_boundary,
                                                 self.dpStopBoundaryX,
                                                 self.dpStopBoundaryY)

    def set_dp_resolution(self):
        self.application_logic.text_field_caller(self.drawing_properties.set_resolution,
                                                 self.dpResolutionX,
                                                 self.dpResolutionY)

    def set_all_newton_properties(self, *properties):
        self.newton_properties.set_all_properties(*properties)


class ApplicationLogic:
    def __init__(self, application_gui):
        self.application_gui = application_gui
        ConsoleLogger.set_output_stream(self.application_gui.consoleTextArea)
        self.consoleLogger = ConsoleLogger.get_instance()
        ResultLogger.set_output_stream(self.application_gui.resultTextArea)
        self.resultLogger = ResultLogger.get_instance()
        self.goal_function = GoalFunction()                         # goal function of an algorithm

    def formula_inserted(self):
        self.application_gui.chooseFunctionComboBox.setCurrentIndex(0)      # reset function chooser
        self.text_field_caller(self.goal_function.set_goal_function,
                               self.application_gui.formulaInput)

    def formula_predefined_inserted(self):
        self.text_field_caller(self.application_gui.goal_function.set_goal_function,
                               self.application_gui.formulaInput)

    def predefined_function_selected(self):
        if self.application_gui.chooseFunctionComboBox.currentIndex() == 0:
            return
        else:
            # choose function and update all properties
            function_name = self.application_gui.chooseFunctionComboBox.currentText()
            print function_name
            expression = PredefinedFunctions.get_function(function_name)
            self.application_gui.formulaInput.setText(expression)
            properties = PredefinedFunctions.get_properties(function_name)
            self.application_gui.set_all_newton_properties(*properties)
            self.application_gui.update_newton_properties_fields()

    def draw(self):
        if not self.goal_function.is_correctly_parsed():        # if function not parsed, return
            return
        self.consoleLogger.log("Drawing function...", LoggerLevel.ADDITIONAL)

        # draw function
        self.application_gui.plotter.plot_function(self.goal_function,
                                                   self.application_gui.drawing_properties)
        self.consoleLogger.log("Drawing function finished", LoggerLevel.ADDITIONAL)

    def run(self):
        """Main loop of a program - it computes next points found with newton algorithm"""
        if not self.goal_function.is_correctly_parsed():        # if function not parsed, return
            return

        self.consoleLogger.log("Execute button pressed", LoggerLevel.NORMAL)
        self.resultLogger.log("Function: " + self.goal_function.get_function_name(), LoggerLevel.NORMAL)
        self.draw()

        newton_algorithm = NewtonAlgorithm(self.goal_function.get_expression(),
                                           *self.application_gui.newton_properties.
                                           get_properties_for_newton_algorithm(),
                                           debug=True)

        # get starting point
        xn = convert_array_to_numpy_point(self.application_gui.newton_properties.
                                          get_starting_point())
        newton_algorithm.set_starting_point_numpy_array(xn)
        min_found = False
        while not min_found:
            self.resultLogger.log("(" + str(xn[0][0]) + ", " + str(xn[1][0]) + ")", LoggerLevel.NORMAL)
            self.resultLogger.log("with value: " + str(self.goal_function.get_expression().
                                  evaluate({'x': xn[0][0], 'y': xn[1][0]})), LoggerLevel.INFO)
            xnn, min_found = newton_algorithm.next_step()
            self.application_gui.plotter.add_numpy_points_to_mesh_grid(xn, xnn)
            xn = xnn

        self.resultLogger.log("minimum found at point: \n(" + str(xn[0][0]) + ", " + str(xn[1][0]) + ")",
                              LoggerLevel.INFO)
        self.resultLogger.log("with value: " + str(self.goal_function.get_expression().
                              evaluate({'x': xn[0][0], 'y': xn[1][0]})), LoggerLevel.INFO)
        self.resultLogger.log("with nr of iterations: " + str(newton_algorithm.get_current_nr_of_iterations()),
							  LoggerLevel.INFO)

    @staticmethod
    def text_field_caller(function, *fields):
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

    @staticmethod
    def toggle_visibility(widget):
        widget.setVisible(not widget.isVisible())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = App()
    form.showMaximized()
    app.exec_()
