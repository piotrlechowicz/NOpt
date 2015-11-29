from optimization_tools import GradientAlgorithm
import numpy as np
from logger.logger import ConsoleLogger, LoggerLevel
from scipy.optimize import minimize_scalar
from utils.numpy_utils import numpy_point_to_string, evaluate_expression_as_string


class NewtonAlgorithm(GradientAlgorithm):
    def __init__(self, expression, start, stop, resolution, tolerance=0.1, debug=False):
        """
        :param expression: expression of the goal function
        :param start: begin of the function range
        :param stop: end of the function range
        :param resolution: resolution of points
        :param tolerance: tolerance of calculations
        :param tau: length of step
        """
        GradientAlgorithm.__init__(self, expression, start, stop, resolution)
        self.console_logger = ConsoleLogger.get_instance()
        self.expression = expression
        self.start = start
        self.stop = stop
        self.tolerance = tolerance
        self.current_point = np.array([[0], [0]])
        self.next_point = np.array([[0], [0]])
        self.iteration = 0
        self.max_nr_of_iterations = 100
        self.minimum_found = False
        self.debug = debug

    def set_starting_point(self, current):
        self.current_point = np.array([[current[0]], [current[1]]])

    def set_starting_point_numpy_array(self, point):
        self.current_point = point

    def set_tolerance(self, tolerance):
        self.tolerance = tolerance

    def set_max_nr_of_iterations(self, max_nr):
        self.max_nr_of_iterations = max_nr

    def get_current_nr_of_iterations(self):
        return self.iteration

    def compute_algorithm(self):
        """run the algorithm"""
        while not self.minimum_found:
            self.__algorithm_step()
        return self.current_point

    def next_step(self):
        """"run one step of an algorithm"""
        if not self.minimum_found:
            self.__algorithm_step()
        return self.current_point, self.minimum_found

    def __algorithm_step(self):
        """actual step of an algorithm"""
        if self.debug:
            self.console_logger.log("Current point: " + numpy_point_to_string(self.current_point),
                                    LoggerLevel.NORMAL)
            self.console_logger.log("With value: " + evaluate_expression_as_string(self.expression,
                                                                                   self.current_point),
                                    LoggerLevel.NORMAL)

        xk = self.current_point[0][0]
        yk = self.current_point[1][0]

        # calculate gradient in current point
        gradient = self.get_gradient_as_array_at(xk, yk)

        # calculate hessian in current point
        hessian = self.get_hessian_as_array_at(xk, yk)

        self.console_logger.log("gradient: " + numpy_point_to_string(gradient),
                                LoggerLevel.NORMAL)

        try:
            # invert hessian
            inv_hessian = np.linalg.inv(hessian)
        except np.linalg.linalg.LinAlgError as error:
            # calculate using steepest descent algorithm
            self.next_point = self.__steepest_descent_next_step(gradient)
        # if no exception
        else:
            # direction of next move
            dk = self.__calculate_next_dk_value(inv_hessian, gradient)

            self.console_logger.log("dk: " + numpy_point_to_string(dk),
                                    LoggerLevel.NORMAL)
            if not self.__is_hessian_spd(dk, gradient):
                # if hessian is not spd calculate next step with descent algorithm
                self.next_point = self.__steepest_descent_next_step(gradient)
            else:
                self.next_point = self.__calculate_next_point(dk)
        finally:
            # if algorithm finished or there are too many iterations
            if self.__is_end_of_algorithm() or self.iteration >= self.max_nr_of_iterations:
                self.minimum_found = True

            self.iteration += 1
            self.current_point = self.next_point

    def __steepest_descent_next_step(self, gradient):
        """calculate next point using steepest descent"""
        print "descent"
        tau = self.__calculate_step_in_direction(-gradient)
        dk = np.multiply(-gradient, tau)
        return np.add(self.current_point, dk)

    @staticmethod
    def __calculate_next_dk_value(inv_hessian, gradient):
        """calculate direction of movment"""
        return -np.dot(inv_hessian, gradient)

    def __calculate_next_point(self, dk):
        """Next point in algorithm"""
        print "newton"
        tau = self.__calculate_step_in_direction(dk)
        return np.add(self.current_point, np.multiply(dk, tau))

    def __is_end_of_algorithm(self):
        """check if algorithm finished"""
        return np.linalg.norm(self.next_point - self.current_point) < self.tolerance

    @staticmethod
    def __is_hessian_spd(dk, gradient):
        """Check if hessian is spd"""
        return (np.dot(np.transpose(gradient), dk) < 0)[0][0]

    def __calculate_step_in_direction(self, dk):
        """Calculate minimum in direction using brnet method"""
        # x_i+1 = x_i + tau * dk

        xtau = "%f + tau * %f" % (self.current_point[0][0], dk[0][0])
        ytau = "%f + tau * %f" % (self.current_point[1][0], dk[1][0])
        expr = self.expression.substitute('x', xtau)        # put it into an expression
        expr = expr.substitute('y', ytau)
        expr = expr.simplify({})                            # simplify that it can be converted to string
        # self.console_logger.log("optimization in direction:\n" + expr.toString(), LoggerLevel.NORMAL)
        fun = lambda tau: expr.evaluate({'tau': tau})       # make it a function
        res = minimize_scalar(fun, tol=0.01)                # minimize using brent method
        tau = res.x                                         # get the value of tau
        self.console_logger.log("value of tau: " + str(tau), LoggerLevel.ADDITIONAL)
        return tau
        # return 1

if __name__ == "__main__":
    from py_expression_eval import Parser
    parser = Parser()
    expr = parser.parse('x^2 + y^3')
    na = NewtonAlgorithm(expr, start=[-6., -6.], stop=[6., 6.], num_of_values=[1001, 1001], debug=True)
    na.set_starting_point([0, 0.5])
    na.set_max_nr_of_iterations(4)
    na.compute_algorithm()
