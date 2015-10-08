class GoalFunction:
    """ Class which holds a goal function to optimize """
    def __init__(self):
        self.variables = ['x', 'y']
        self.expression = ""
        self.function_name = ""

    def fetch_function_name(self):
        self.function_name = self.expression.simplify({}).toString()[1:-1]
