from docutils.nodes import paragraph

__author__ = 'Piotr Lechowicz'

import sys

try:
    from py_expression_eval import Parser
except ImportError as error:
    print error.message
    sys.exit("Not all the requirements are fulfilled")


from expression.goal_function import GoalFunction
from expression.validate import ExpressionValidator
from plot.plot import Plotter
from optimization.newton import NewtonAlgorithm
from numpy import array

# Interesting function: (x+1)^2 * (y-1)^4 + (y+1)^4 * (x-1)^2

class App:
    def __init__(self):
        pass

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
            print "enter: start, stop, num_od_values_for_drawing"
            input = raw_input()
            input = input.split(',')
            parameters_dr = []
            if input.__len__() > 1:
                for par in input:
                    par = float(par)
                    parameters_dr.append([par, par])
            else:
                parameters_dr.extend([[-4., -4.], [4., 4.], [101, 101]])

            # get newton algorithm parameters
            print "enter: start, stop, num_of_values_for_newton"
            input = raw_input()
            input = input.split(',')
            parameters_na = []
            if input.__len__() > 1:
                for par in input:
                    par = float(par)
                    parameters_na.append([par, par])
            else:
                parameters_na.extend([[-4., -4.], [4., 4.], [1001, 1001]])

            # plot function
            print goal_function.function_name
            plotter = Plotter(goal_function.expression, goal_function.function_name, *parameters_dr)
            plotter.plot_function_in_3D()

            na = NewtonAlgorithm(goal_function.expression, *parameters_na, debug=True)
            xn = array([[3.], [3.5]])
            na.set_starting_point_numpy_array(xn)
            min_found = False
            while not min_found:
                xnn, min_found = na.next_step()
                plotter.add_to_result_numpy_points(xn, xnn)
                xn = xnn

            plotter.wait_to_close_plot_windows()


if __name__ == "__main__":
    app = App()
    app.run()
