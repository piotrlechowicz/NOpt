from numpy import array


def convert_array_to_numpy_point(point):
    assert isinstance(point, list)
    assert len(point) >= 2
    return array([[point[0]], [point[1]]])
