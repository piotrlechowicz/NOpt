class Properties:
    """Abstract class of necessary properties"""
    def __init__(self):
        self.start_boundary = [-5., -5.]
        self.stop_boundary = [5., 5.]
        self.resolution = [0.1, 0.1]

    def set_default_values(self):
        self.start_boundary = [-5., -5.]
        self.stop_boundary = [5., 5.]
        self.resolution = [0.1, 0.1]

    def set_start_boundary(self, x, y):
        try:
            x = float(x)
            y = float(y)
            self.start_boundary = [x, y]
            return True
        except ValueError:
            return False

    def set_stop_boundary(self, x, y):
        try:
            x = float(x)
            y = float(y)
            self.stop_boundary = [x, y]
            return True
        except ValueError:
            return False

    def set_resolution(self, x, y):
        try:
            x = float(x)
            y = float(y)
            self.resolution = [x, y]
            return True
        except ValueError:
            return False

    def get_all_properties(self):
        return [self.start_boundary, self.stop_boundary, self.resolution]


class NewtonAlgorithmProperties(Properties):
    def __init__(self):
        Properties.__init__(self)
        self.starting_point = [1., 1.]
        self.tolerance = 0.1

    def __set_default_values(self):
        Properties.set_default_values(self)
        self.starting_point = [1., 1.]
        self.tolerance = 0.1

    def set_starting_point(self, x, y):
        try:
            x = float(x)
            y = float(y)
            self.starting_point = [x, y]
            return True
        except ValueError:
            return False

    def set_tolerance(self, tolerance):
        try:
            tolerance = float(tolerance)
            self.tolerance = tolerance
            return True
        except ValueError:
            return False

    def get_all_properties(self):
        properties = Properties.get_all_properties(self)
        properties.insert(0, self.starting_point)
        properties.append(self.tolerance)
        return properties


class DrawingProperties(Properties):
    def __init__(self):
        Properties.__init__(self)
        self.max_nr_of_points = 1000
        self.resolution = [0.5, 0.5]

    def set_resolution(self, x, y):
        try:
            x = float(x)
            y = float(y)
            if (self.stop_boundary[0] - self.start_boundary[0]) / x > self.max_nr_of_points:
                x = self.stop_boundary[0] - self.start_boundary[0] / self.max_nr_of_points
            if (self.stop_boundary[1] - self.start_boundary[1]) / x > self.max_nr_of_points:
                y = self.stop_boundary[1] - self.start_boundary[1] / self.max_nr_of_points
            self.resolution = [x, y]
            return True
        except (ValueError, ZeroDivisionError):
            return False
