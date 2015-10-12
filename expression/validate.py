class ExpressionValidator:
    """Validates an user's input according to the variables in the goal expression

        @return expression, validates, validation_error
    """
    def __init__(self, expression, variables=['x', 'y']):
        self.constants = {"pi":  3.14159265358979323846,
                          "e": 2.71828182845904523536}
        self.validates = True
        self.variables = variables
        self.expr = expression
        self.all_expr_variables = self.expr.variables()
        self.validation_error = ""

    def validate(self):
        self.__evaluate_constants()
        self.__contains_correct_number_of_variables()
        self.__has_variables()
        return self.expr, self.validates, self.validation_error

    def __evaluate_constants(self):
        for (key, value) in self.constants.items():
            if key in self.all_expr_variables:
                self.expr = self.expr.simplify({key: value})
        # update list of all variables
        self.all_expr_variables = self.expr.variables()

    def __has_variables(self):
        for var in self.all_expr_variables:
            if var not in self.variables:
                self.validation_error += "Unknown constant: " + var + "\n"
                self.validates = False

    def __contains_correct_number_of_variables(self):
        if self.all_expr_variables.__len__() is not self.variables.__len__():
            self.validation_error += "Function must contain exactly " + str(self.variables.__len__()) + " variables:"
            for var in self.variables:
                self.validation_error += " '" + var + "'"
            self.validation_error += "\n"
            self.validates = False
