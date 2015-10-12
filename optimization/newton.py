from optimization_tools import GradientAlgorithm
import numpy as np


class NewtonAlgorithm(GradientAlgorithm):
    def __init__(self, expression, start, stop, num_of_values, tolerance=0.1, tau=1, debug=False):
        """
        :param expression: expression of the goal function
        :param start: begin of the function range
        :param stop: end of the function range
        :param num_of_values: number of values in range
        :param tolerance: tolerance of calculations
        :param tau: length of step
        """
        GradientAlgorithm.__init__(self, expression, start, stop, num_of_values)
        self.start = start
        self.stop = stop
        self.tolerance = tolerance
        self.tau = tau
        self.current_point = np.array([[0, 0]])
        self.next_point = np.array([[0, 0]])
        self.iteration = 0
        self.max_nr_of_iterations = 100

        self.debug = debug

    def set_starting_point(self, current):
        self.current_point = np.array([[current[0], current[1]]])

    def set_tolerance(self, tolerance):
        self.tolerance = tolerance

    def set_max_nr_of_iterations(self, max_nr):
        self.max_nr_of_iterations = max_nr

    def start_algorithm(self):
        while True:
            self.iteration += 1

            xn = self.current_point[0][0]
            yn = self.current_point[0][1]

            hessian = self.get_hessian_as_array_at(xn, yn)
            # TODO: what if inv hessian can't be calculated
            # TODO: numpy.linalg.linalg.LinAlgError -> compute next move using just gradient
            inv_hessian = np.linalg.inv(hessian)

            gradient = self.get_gradient_as_array_at(xn, yn)

            if self.debug:
                print "Matrix inversion: "
                print np.dot(hessian, inv_hessian)
                print "Hessian and inv hessian: "
                print hessian
                print inv_hessian
                print "Gradient: "
                print gradient
                print "InvHess * grad"
                mul = np.transpose(np.dot(inv_hessian, np.transpose(gradient)))
                print mul
                print "xn - inv*grad"
                print np.subtract(self.current_point, mul)

            

            # self.next_point = np.subtract(
            #     self.current_point -
            #     self.get_hessian_as_array_at(self.star)
            if self.__is_end_of_algorithm() or self.iteration > self.max_nr_of_iterations:
                break


    def __calculate_next_point(self):
        pass

    def __is_end_of_algorithm(self):
        return np.linalg.norm(self.next_point - self.current_point) < self.tolerance


if __name__ == "__main__":
    from py_expression_eval import Parser
    parser = Parser()
    expr = parser.parse('x^2 + y^3')
    na = NewtonAlgorithm(expr, start=[-2., -2.], stop=[2., 2.], num_of_values=[101, 101], debug=True)
    na.set_starting_point([0, 0.5])
    na.set_max_nr_of_iterations(4)
    na.start_algorithm()

