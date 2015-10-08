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

            # plot function
            print goal_function.function_name
            plotter = Plotter()
            plotter.plot(goal_function.expression, goal_function.function_name)


if __name__ == "__main__":
    app = App()
    app.run()
