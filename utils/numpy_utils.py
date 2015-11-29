import sys

try:
    import numpy
except ImportError as error:
    print "numpy is necessary"
    print error.message
    sys.exit(1)

numpy_version = numpy.__version__.split(',')
if numpy_version < [1, 10, 1]:
    print "numpy in version 1.10.1 or greater is required"
    sys.exit(1)


def convert_array_to_numpy_point(point):
    assert isinstance(point, list)
    assert len(point) >= 2
    return numpy.array([[point[0]], [point[1]]])


def numpy_point_to_string(point):
    return "(" + str(point[0][0]) + ", " + str(point[1][0]) + ")"


def evaluate_expression_as_string(expression, point):
    return str(expression.evaluate({'x': point[0][0],
                                    'y': point[1][0]}))
