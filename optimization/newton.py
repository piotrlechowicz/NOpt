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
        self.current_point = np.array([[0], [0]])
        self.next_point = np.array([[0], [0]])
        self.iteration = 0
        self.max_nr_of_iterations = 100
        self.minimum_found = False

        self.debug = debug

    def set_starting_point(self, current):
        self.current_point = np.array([[current[0]], [current[1]]])

    def set_tolerance(self, tolerance):
        self.tolerance = tolerance

    def set_max_nr_of_iterations(self, max_nr):
        self.max_nr_of_iterations = max_nr

    def compute_algorithm(self):
        while not self.minimum_found:
            self.__algorithm_step()
        return self.current_point

    def next_step(self):
        if not self.minimum_found:
            self.__algorithm_step()
        return self.current_point, self.minimum_found

    def __algorithm_step(self):
        xk = self.current_point[0][0]
        yk = self.current_point[1][0]

        gradient = self.get_gradient_as_array_at(xk, yk)

        hessian = self.get_hessian_as_array_at(xk, yk)
        # TODO: what if inv hessian can't be calculated
        # TODO: numpy.linalg.linalg.LinAlgError -> compute next move using just gradient
        try:
            inv_hessian = np.linalg.inv(hessian)
        except np.linalg.linalg.LinAlgError as error:
            # calculate using steepest descent algorithm
            self.next_point = self.__steepest_descent_next_step(gradient)
            if self.debug:
                print "Next point (gradient): "
                print self.next_point
        else:
            dk = self.__calculate_next_dk_value_newton(inv_hessian, gradient)
            if not self.__is_hessian_spd(dk, gradient):
                self.next_point = self.__steepest_descent_next_step(gradient)
            else:
                self.next_point = self.__calculate_next_point_newton(dk)

            if self.debug:
                print "Hessian spd?: "
                print self.__is_hessian_spd(dk, gradient)
                print "Next point: "
                print self.next_point

        finally:
            if self.__is_end_of_algorithm() or self.iteration >= self.max_nr_of_iterations:
                self.minimum_found = True

            self.iteration += 1
            self.current_point = self.next_point

    def __steepest_descent_next_step(self, gradient):
        # TODO: minimize dk as a search of best tau
        dk = (-gradient) * self.tau
        return np.add(self.current_point, dk)


    def __calculate_next_dk_value_newton(self, inv_hessian, gradient):
        return -np.dot(inv_hessian, gradient)

    def __calculate_next_point_newton(self, dk):
        return np.add(self.current_point, np.multiply(dk, self.tau))

    def __is_end_of_algorithm(self):
        # TODO: change that end is only based on the dn value, not including step tau
        return np.linalg.norm(self.next_point - self.current_point) < self.tolerance

    def __is_hessian_spd(self, dk, gradient):
        return (np.dot(np.transpose(gradient), dk) < 0)[0][0]


if __name__ == "__main__":
    from py_expression_eval import Parser
    parser = Parser()
    expr = parser.parse('x^2 + y^3')
    na = NewtonAlgorithm(expr, start=[-6., -6.], stop=[6., 6.], num_of_values=[1001, 1001], debug=True)
    na.set_starting_point([0, 0.5])
    na.set_max_nr_of_iterations(4)
    na.compute_algorithm()

