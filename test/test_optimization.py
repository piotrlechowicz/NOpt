import unittest
from py_expression_eval import Parser
from optimization.optimization_tools import OptimizationAlgorithm,\
    GradientAlgorithm
import numpy as np


class TestOptimizationAlgorithm(unittest.TestCase):

    def setUp(self):
        self.parser = Parser()
        make_expr = lambda string, start, stop, num_of_val1, num_of_val2: \
            [self.parser.parse(string), [start, start],
                [stop, stop], [num_of_val1, num_of_val2]]
        self.expressions = [make_expr('x^2 + y^3', -4., 4., 801, 701),
                            make_expr('y^2*sin(x) + 2*y^4', -4., 4., 1001, 901)]
        self.tests_values = [[[-2., -2.], [1., 2.5], [-1.5, 0]],
                             [[1., 1.], [-1.5, 2.5]]]
        self.answers_values = [[[-4.0], [16.625], [2.25]],
                               [[2.841], [71.89]]]

        self.tests_gradient = [[[-2., -2.], [0., -1.5]],
                               [[1.3, -0.5], [-0.5, 1]]]
        self.answers_gradient = [[[-4., 12.], [0., 6.75]],
                                 [[0.0669, -1.9635], [0.8776, 7.0411]]]

        self.tests_hessian = [[[-2., 1.5]],
                              [[-2, 1.5]]]
        self.answers_hessian = [[[2., 0, 0, 9.]],
                                [[2.046, -1.248, -1.248, 52.181]]]

    def testValues(self):
        for i in range(self.expressions.__len__()):
            self.opt_alg = OptimizationAlgorithm(*self.expressions[i])
            for (test, answer) in zip(self.tests_values[i], self.answers_values[i]):
                self.assertAlmostEqual(answer, self.opt_alg.value_at(*test), delta=0.1)

    def testGradient(self):
        for i in range(self.expressions.__len__()):
            self.grad_alg = GradientAlgorithm(*self.expressions[i])
            for (test, answer) in zip(self.tests_gradient[i], self.answers_gradient[i]):
                gx, gy = self.grad_alg.get_gradient_at(*test)
                self.assertAlmostEqual(answer[0], gx, delta=0.1)
                self.assertAlmostEqual(answer[1], gy, delta=0.1)

    def testGradientArray(self):
        for i in range(self.expressions.__len__()):
            self.grad_alg = GradientAlgorithm(*self.expressions[i])
            for (test, answer) in zip(self.tests_gradient[i], self.answers_gradient[i]):
                grad = self.grad_alg.get_gradient_as_array_at(*test)
                self.assertAlmostEqual(answer[0], grad[0][0], delta=0.1)
                self.assertAlmostEqual(answer[1], grad[0][1], delta=0.2)

    def testHessian(self):
        for i in range(self.expressions.__len__()):
            self.grad_alg = GradientAlgorithm(*self.expressions[i])
            for (test, answer) in zip(self.tests_hessian[i], self.answers_hessian[i]):
                gxx, gxy, gyx, gyy = self.grad_alg.get_hessian_at(*test)
                self.assertAlmostEquals(answer[0], gxx, delta=0.1)
                self.assertAlmostEquals(answer[1], gxy, delta=0.1)
                self.assertAlmostEquals(answer[2], gyx, delta=0.1)
                self.assertAlmostEquals(answer[3], gyy, delta=0.1)

    def testHessianArray(self):
        for i in range(self.expressions.__len__()):
            self.grad_alg = GradientAlgorithm(*self.expressions[i])
            for (test, answer) in zip(self.tests_hessian[i], self.answers_hessian[i]):
                hessian = self.grad_alg.get_hessian_as_array_at(*test)
                self.assertAlmostEquals(answer[0], hessian[0][0], delta=0.1)
                self.assertAlmostEquals(answer[1], hessian[0][1], delta=0.1)
                self.assertAlmostEquals(answer[2], hessian[1][0], delta=0.1)
                self.assertAlmostEquals(answer[3], hessian[1][1], delta=0.1)


if __name__ == "__main__":
    unittest.main()
