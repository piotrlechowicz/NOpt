__author__ = 'Piotr Lechowicz'

import sys

try:
    from py_expression_eval import Parser
    # import numpy
except ImportError as error:
    print error.message
    sys.exit("Not all the requirements are fulfilled")


class App:
    def __init__(self):
        pass

    def run(self):
        # main program loop
        while True:
            print "Enter a goal function"
            user_input = raw_input()
            print user_input
            if user_input == "quit":
                break

            # application logic
            goal_function = GoalFunction()
            parser = Parser()
            try:
                goal_function.expression = parser.parse(user_input)
            except Exception as exception:
                print exception.message
                continue

            expression_validator = ExpressionValidator(goal_function.expression, goal_function.variables)
            goal_function.expression, validates, validation_error = expression_validator.validate()

            if not validates:
                print validation_error
                continue

            print goal_function.expression.toString()


class GoalFunction:
    """ Class which holds a goal function to optimize """
    def __init__(self):
        self.variables = ['x', 'y']
        self.expression = ""


class ExpressionValidator:
    """Validates an user's input according to the variables in the goal function

        @return expression, validates, validation_error
    """
    def __init__(self, expression, variables):
        self.constants = {"pi":  3.14159265358979323846,
                          "e": 2.71828182845904523536}
        self.validates = True
        self.variables = variables
        self.expr = expression
        self.all_expr_variables = self.expr.variables()
        self.validation_error = ""

    def validate(self):
        self.evaluate_constants()
        self.contains_correct_number_of_variables()
        self.has_variables()
        return self.expr, self.validates, self.validation_error

    def evaluate_constants(self):
        for (key, value) in self.constants.items():
            if key in self.all_expr_variables:
                self.expr = self.expr.simplify({key: value})
        # update list of all variables
        self.all_expr_variables = self.expr.variables()

    def has_variables(self):
        for var in self.all_expr_variables:
            if var not in self.variables:
                self.validation_error += "Unknown constant: " + var + "\n"
                self.validates = False

    def contains_correct_number_of_variables(self):
        if self.all_expr_variables.__len__() is not self.variables.__len__():
            self.validation_error += "Function must contain exactly " + str(self.variables.__len__()) + " variables:"
            for var in self.variables:
                self.validation_error += " '" + var + "'"
            self.validation_error += "\n"
            self.validates = False


if __name__ == "__main__":
    app = App()
    app.run()
