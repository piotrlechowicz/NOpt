import numpy as np


def vectorize_expression(expression):
    return np.vectorize(lambda x, y: expression.evaluate({'x': x, 'y': y}))


class OptimizationAlgorithm:
    def __init__(self, expression, start=[-1., -1.], stop=[1., 1.], num_of_values=[101, 101]):
        self.evaluate = vectorize_expression(expression)
        self.start_x, self.start_y = start
        self.stop_x, self.stop_y = stop
        self.num_of_values_x, self.num_of_values_y = num_of_values
        self.x = self.y = None
        self.mx = self.my = None
        self.z = None
        self.dx = self.dy = None

        self.__create_mesh()
        self.__calculate_values()

    def __create_mesh(self):
        self.x = np.linspace(self.start_x, self.stop_x, self.num_of_values_x)
        self.y = np.linspace(self.start_y, self.stop_y, self.num_of_values_y)
        self.dx = (self.stop_x - self.start_x) / self.num_of_values_x
        self.dy = (self.stop_y - self.start_y) / self.num_of_values_y

        self.mx, self.my = np.meshgrid(self.x, self.y)

    def __calculate_values(self):
        self.z = self.evaluate(self.mx, self.my)

    def get_id_of_x(self, value):
        index = int((value - self.start_x) / self.dx)
        if index < 0:
            index = 0
        elif index >= self.num_of_values_x:
            index = self.num_of_values_x - 1
        return index

    def get_id_of_y(self, value):
        index = int((value - self.start_y) / self.dy)
        if index < 0:
            index = 0
        elif index >= self.num_of_values_y:
            index = self.num_of_values_y - 1
        return index

    def get_evaluated_function(self):
        return self.z

    def value_at(self, x, y):
        id_x = self.get_id_of_x(x)
        id_y = self.get_id_of_y(y)
        return self.z[id_y][id_x]


class GradientAlgorithm(OptimizationAlgorithm):
    def __init__(self, expression, start, stop, num_of_values):
        OptimizationAlgorithm.__init__(self, expression, start, stop, num_of_values)
        self.diff_tools = DiffTools(self.z, self.dx, self.dy)
        self.__initialize_diff_tools()

    def get_gradient_at(self, x, y):
        id_x = self.get_id_of_x(x)
        id_y = self.get_id_of_y(y)
        return self.diff_tools.get_gradient_at_id(id_x, id_y)

    def get_gradient_as_array_at(self, x, y):
        gx, gy = self.get_gradient_at(x, y)
        return np.array([[gx, gy]])

    def get_hessian_at(self, x, y):
        id_x = self.get_id_of_x(x)
        id_y = self.get_id_of_y(y)
        return self.diff_tools.get_hessian_at_id(id_x, id_y)

    def get_hessian_as_array_at(self, x, y):
        gxx, gxy, gyx, gyy = self.get_hessian_at(x, y)
        return np.array([[gxx, gxy], [gyx, gyy]])

    def __initialize_diff_tools(self):
        self.diff_tools.calculate_gradient()
        self.diff_tools.calculate_hessian()


class DiffTools:
    def __init__(self, function_values, dx, dy):
        self.z = function_values
        self.dx = dx
        self.dy = dy
        self.gx = None
        self.gy = None
        self.gxx = None
        self.gxy = None
        self.gyx = None
        self.gyy = None

    def calculate_gradient(self):
        self.gy, self.gx = np.gradient(self.z, self.dy, self.dx)

    def calculate_hessian(self):
        self.gxy, self.gxx = np.gradient(self.gx, self.dy, self.dx)
        self.gyy, self.gyx = np.gradient(self.gy, self.dy, self.dx)

    def get_gradient_at_id(self, id_x, id_y):
        return self.gx[id_y][id_x], self.gy[id_y][id_x]

    def get_hessian_at_id(self, id_x, id_y):
        return self.gxx[id_y][id_x], self.gxy[id_y][id_x],\
            self.gyx[id_y][id_x], self.gyy[id_y][id_x]


if __name__ == "__main__":
    from py_expression_eval import Parser
    parser = Parser()
    expr = parser.parse('x^2 + y^3*x')
    ga = GradientAlgorithm(expr, [-4., -4.], [4., 4.], [801, 801])
    print "---------------------------"
    print "Gradient: "
    print ga.get_gradient_at(-2., -1.)
    print ga.get_gradient_as_array_at(-2., -1.)
    print "---------------------------"
    print "Hessian: "
    print ga.get_hessian_at(-2., -1.)
    print ga.get_hessian_as_array_at(-2., -1.)
