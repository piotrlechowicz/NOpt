import sys
try:
    from py_expression_eval import Parser
except ImportError as error:
    print error.message
    print "py_expression_eval is necessary"
    sys.exit("Not all the requirements are fulfilled")
from expression.validate import ExpressionValidator
from logger.logger import ConsoleLogger, LoggerLevel


class GoalFunction:
    """ Class which holds a goal function to optimize """
    def __init__(self, initial_function=None):
        self.console_logger = ConsoleLogger.get_instance()  # get logger
        self.console_logger.log("Goal function initializing...", LoggerLevel.DEBUG)
        self.__expression = ""                              # function expression
        self.__function_name = ""                           # function simple name
        self.__variables = ['x', 'y']                       # variables in function
        self.__parser = Parser()                            # function parser
        self.__correctly_parsed = True                      # whether the function was correctly parsed
        self.set_goal_function("x ^ 4 * (y + 1) ^ 2 + y ^ 4 * (x + 1) ^ 2")     # set some default function
        if initial_function:                                                    # if to constructor was passed function
            self.set_goal_function(initial_function)                            # try to set it
        self.console_logger.log("Goal function initialized", LoggerLevel.DEBUG)

    def __fetch_function_name(self):
        self.__function_name = self.__expression.simplify({}).toString()[1:-1]
        self.console_logger.log("function fetched to: " + self.get_function_name(), LoggerLevel.ADDITIONAL)

    def get_function_name(self):
        return self.__function_name

    def get_expression(self):
        return self.__expression

    def is_correctly_parsed(self):
        return self.__correctly_parsed

    def set_goal_function(self, function):
        """sets goal function

        If function is not correctly set it returns false,
        if it is correctly set itt returns true
        """
        try:
            function = function.lower()                                       # convert input to lower case
            expression = self.__parser.parse(function)                        # try to parse expression

            validator = ExpressionValidator(expression, self.__variables)     # get expression validator
            expression, validates, validation_error = validator.validate()    # expression validation
            if not validates:
                self.console_logger.log("function is not validating", LoggerLevel.ERROR)
                self.console_logger.log(validation_error, LoggerLevel.ERROR)
                print validation_error
                raise Exception()
            self.__expression = expression
            self.__fetch_function_name()                                   # fetch simple name from function
            self.console_logger.log("function: " + self.get_expression().toString(), LoggerLevel.ADDITIONAL)
            self.__correctly_parsed = True
            return True
        except Exception:
            self.__correctly_parsed = False
            return False
