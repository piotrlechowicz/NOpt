from numpy import array


def convert_array_to_numpy_point(point):
    assert isinstance(point, list)
    assert len(point) >= 2
    return array([[point[0]], [point[1]]])


def numpy_point_to_string(point):
    return "(" + str(point[0][0]) + ", " + str(point[1][0]) + ")"


def evaluate_expression_as_string(expression, point):
    return str(expression.evaluate({'x': point[0][0],
                                    'y': point[1][0]}))
