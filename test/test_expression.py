import unittest
from py_expression_eval import Parser
from expression.validate import ExpressionValidator
from expression.goal_function import GoalFunction


class TestExpressions(unittest.TestCase):

    def setUp(self):
        self.parser = Parser()
        self.goal_functions = [self.get_goal_function('x^2 + y ^ 3'),
                               self.get_goal_function('sin(e)*x*y + e*y')]
        self.answers = [['((x^2.0)+(y^3.0))', '(x^2.0)+(y^3.0)', True],
                        ['(((0.410781290503*x)*y)+(2.71828182846*y))',
                         '((sin(e)*x)*y)+(e*y)',
                         True]]

        self.goal_err_functions = [self.get_goal_function('x^2 + z'),
                                   self.get_goal_function('x + a + y')]

    def get_goal_function(self, expression):
        gf = GoalFunction()
        gf.__expression = self.parser.parse(expression)
        gf.__fetch_function_name()
        return gf

    def testExpressionValidation(self):
        for (gf, answers) in zip(self.goal_functions, self.answers):
            expr, validates, val_error = ExpressionValidator(gf.expression).validate()
            self.assertEqual(answers[0], expr.toString())
            self.assertEqual(answers[1], gf.get_function_name())
            self.assertTrue(validates)

    def testExpressionFailure(self):
        for gf in self.goal_err_functions:
            expr, validates, val_error = ExpressionValidator(gf.__expression).validate()
            self.assertFalse(validates)
