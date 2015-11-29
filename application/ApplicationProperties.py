from logger.logger import ConsoleLogger, LoggerLevel


class Properties:
    """Abstract class of necessary properties"""
    def __init__(self):
        self.console_logger = ConsoleLogger.get_instance()
        self.console_logger.log("Base class properties initializing...", LoggerLevel.DEBUG)
        self.start_boundary = [-5., -5.]
        self.stop_boundary = [5., 5.]
        self.resolution = [0.1, 0.1]
        self.console_logger.log("Base class properties initialized", LoggerLevel.DEBUG)

    def set_default_values(self):
        self.start_boundary = [-5., -5.]
        self.stop_boundary = [5., 5.]
        self.resolution = [0.1, 0.1]

    def set_start_boundary(self, x, y):
        try:
            x = float(x)
            y = float(y)
            self.start_boundary = [x, y]
            self.console_logger.log("Start boundary set", LoggerLevel.ADDITIONAL)
            return True
        except ValueError:
            self.console_logger.log("Unable to set start boundary", LoggerLevel.WARN)
            return False

    def set_stop_boundary(self, x, y):
        try:
            x = float(x)
            y = float(y)
            self.stop_boundary = [x, y]
            self.console_logger.log("Stop boundary set", LoggerLevel.ADDITIONAL)
            return True
        except ValueError:
            self.console_logger.log("Unable to set stop boundary", LoggerLevel.WARN)
            return False

    def set_resolution(self, x, y):
        try:
            x = float(x)
            y = float(y)
            if x == 0 or y == 0:
                raise ValueError
            self.resolution = [x, y]
            self.console_logger.log("Resolution set", LoggerLevel.ADDITIONAL)
            return True
        except ValueError:
            self.console_logger.log("Unable to set resolution", LoggerLevel.WARN)
            return False

    def get_all_properties(self):
        return [self.start_boundary, self.stop_boundary, self.resolution]


class NewtonAlgorithmProperties(Properties):
    def __init__(self):
        Properties.__init__(self)
        self.console_logger.log("Newton algorithm properties initializing...", LoggerLevel.DEBUG)
        self.starting_point = [1., 1.]
        self.tolerance = 0.1
        self.console_logger.log("Newton algorithm properties initialized", LoggerLevel.DEBUG)

    def __set_default_values(self):
        Properties.set_default_values(self)
        self.starting_point = [1., 1.]
        self.tolerance = 0.1

    def set_starting_point(self, x, y):
        try:
            x = float(x)
            y = float(y)
            self.starting_point = [x, y]
            self.console_logger.log("Starting point set", LoggerLevel.ADDITIONAL)
            return True
        except ValueError:
            return False

    def set_tolerance(self, tolerance):
        try:
            tolerance = float(tolerance)
            self.tolerance = tolerance
            self.console_logger.log("Tolerance set", LoggerLevel.ADDITIONAL)
            return True
        except ValueError:
            self.console_logger.log("Unable to set tolerance", LoggerLevel.WARN)
            return False

    def get_all_properties(self):
        properties = Properties.get_all_properties(self)
        properties.insert(0, self.starting_point)
        properties.append(self.tolerance)
        return properties

    def get_properties_for_newton_algorithm(self):
        properties = Properties.get_all_properties(self)
        properties.append(self.tolerance)
        return properties

    def get_starting_point(self):
        return self.starting_point


class DrawingProperties(Properties):
    def __init__(self):
        Properties.__init__(self)
        self.console_logger.log("Drawing properties initializing...", LoggerLevel.DEBUG)
        self.max_nr_of_points = 1000
        self.resolution = [0.5, 0.5]
        self.console_logger.log("Drawing properties initialized", LoggerLevel.DEBUG)

    def set_resolution(self, x, y):
        try:
            x = float(x)
            y = float(y)
            if (self.stop_boundary[0] - self.start_boundary[0]) / x > self.max_nr_of_points:
                x = self.stop_boundary[0] - self.start_boundary[0] / self.max_nr_of_points
            if (self.stop_boundary[1] - self.start_boundary[1]) / y > self.max_nr_of_points:
                y = self.stop_boundary[1] - self.start_boundary[1] / self.max_nr_of_points
            self.resolution = [x, y]
            self.console_logger.log("Resolution set", LoggerLevel.ADDITIONAL)
            return True
        except (ValueError, ZeroDivisionError):
            self.console_logger.log("Unable to set resolution", LoggerLevel.WARN)
            return False
