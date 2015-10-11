import numpy as np


def vectorize_expression(expression):
    return np.vectorize(lambda x, y: expression.evaluate({'x': x, 'y': y}))


class GradientAlgorithm:
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

        self.diff_tools = DiffTools(self.z, self.dx, self.dy)

    def __create_mesh(self):
        self.x = np.linspace(self.start_x, self.stop_x, self.num_of_values_x)
        self.y = np.linspace(self.start_y, self.stop_y, self.num_of_values_y)
        self.dx = (self.stop_x - self.start_x) / self.num_of_values_x
        self.dy = (self.stop_y - self.start_y) / self.num_of_values_y

        self.mx, self.my = np.meshgrid(self.x, self.y)

    def __calculate_values(self):
        self.z = self.evaluate(self.mx, self.my)
        print self.z[0][0]

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
        return self.z[id_x][id_y]

    def get_gradient_at(self):
        pass

    def get_hessian_at(self):
        pass


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

    def gradient(self):
        gy, gx = np.gradient(self.z, self.dx, self.dy)

    def hessian(self):
        gxy, gxx = np.gradient(self.gx, self.dx, self.dy)
        gyy, gyx = np.gradient(self.gy, self.dx, self.dy)


if __name__ == "__main__":
    pass