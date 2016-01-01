class PredefinedFunctions:
    def __init__(self):
        pass

    @staticmethod
    def get_function(function_name):
        # optimum f(0, 0) = 0
        if function_name == FunctionNames.ACKLEYS:
            return "-20*exp(-0.2*sqrt(0.5*(x^2 + y^2))) - " +\
                   "exp(0.5*(cos(2*pi*x) + cos(2*pi*y))) + e + 20"
        # optimum f(0, 0) = 0
        elif function_name == FunctionNames.SPHERE:
            return "x^2 + y^2"
        # optimum f(1, 1) = 0
        elif function_name == FunctionNames.ROSENBROCK:
            return "100 * (y - x ^ 2) ^ 2 + (x - 1) ^ 2"
        # optimum f(3, 0.5) = 0
        elif function_name == FunctionNames.BEALES:
            return "(1.5 - x + x*y)^2 + (2.25 - x + x*y^2)^2 " \
                   "+ (2.625 - x + x*y^3)^2"
        # optimum f(0, -1) = 3
        elif function_name == FunctionNames.GOLDSTEIN_PRICE:
            return "(1 + (x + y + 1)^2 * (19 - 14*x + 3*x^2 - 14*y + 6*x*y + 3*y*2))*" +\
                   "(30 + (2*x - 3*y)^2 * (18 - 32*x + 12*x^2 + 48*y - 36*x*y + 27*y^2))"
        # optimum f(1, 3) = 0
        elif function_name == FunctionNames.BOOTHS:
            return "(x + 2*y - 7)^2 + (2*x + y - 5)^2"
        # optimum f(-10, 1) = 0
        elif function_name == FunctionNames.BUKIN:
            return "100*sqrt(abs(y - 0.001*x^2)) + 0.01*abs(x + 10)"
        # optimum f(0, 0) =0
        elif function_name == FunctionNames.MATYAS:
            return "0.26*(x^2 + y^2) - 0.48*x*y"
        # optimum f(1, 1) = 0
        elif function_name == FunctionNames.LEVI:
            return "(sin(3*pi*x))^2 + (x - 1)^2 * (1 + (sin(3*pi*y))^2) +" +\
                   "(y - 1)^2 * (1 + (sin(2*pi*y))^2)"
        # optimum f(pi, pi) = -1
        elif function_name == FunctionNames.EASOM:
            return "-cos(x) * cos(y) * exp(-((x - pi)^2 + (y - pi)^2))"
        # optimum f(+-1.35, +-1.35) = -2.06
        elif function_name == FunctionNames.CROSS_IN_TRAY:
            return "-0.0001*(abs(sin(x)*sin(y)*exp(abs(100 - sqrt(x^2 + y^2)/pi))) + 1)^0.1"
        # optimum f(+-8.05, +-9.66) = -19.21
        elif function_name == FunctionNames.HOLDER:
            return "-abs(sin(x)*cos(y)*exp(abs(1 - sqrt(x^2 + y^2)/pi)))"
        # optimum f(-0.547, -1.547) = -1.913
        elif function_name == FunctionNames.MC_CORNIC:
            return "sin(x + y) + (x - y)^2 - 1.5*x + 2.5*y + 1"
        # optimum f(0, 1.253) = 0.292
        elif function_name == FunctionNames.SCHAFFER:
            return "0.5 + ((cos(sin(abs(x^2 - y^2))))^2 - 0.5)/((1 + 0.001*(x^2 + y^2))^2)"
        # optimum f(+- 2.90, +- 2.90) = -78.332
        elif function_name == FunctionNames.STYBLINSKI_TANG:
            return "(x^4 - 16*x^2 + 5*x + y^4 - 16*y^2 + 5*y)/2"
        else:
            return "x^2 + y^2 + 1"

    @staticmethod
    def get_properties(function_name):
        if function_name == FunctionNames.ACKLEYS:
            return [[-5., -5.], [5., 5.], [0.1, 0.1]]
        elif function_name == FunctionNames.SPHERE:
            return [[-5., -5.], [5., 5.], [0.1, 0.1]]
        if function_name == FunctionNames.ROSENBROCK:
            return [[-5., -5.], [5., 5.], [0.1, 0.1]]
        elif function_name == FunctionNames.BEALES:
            return [[-4.5, -4.5], [4.5, 4.5], [0.1, 0.1]]
        if function_name == FunctionNames.GOLDSTEIN_PRICE:
            return [[-2., -2.], [2., 2.], [0.1, 0.1]]
        elif function_name == FunctionNames.BOOTHS:
            return [[-10., -10.], [10., 10.], [0.1, 0.1]]
        if function_name == FunctionNames.BUKIN:
            return [[-15., -3.], [-5., 3.], [0.1, 0.1]]
        elif function_name == FunctionNames.MATYAS:
            return [[-10., -10.], [10., 10.], [0.1, 0.1]]
        if function_name == FunctionNames.LEVI:
            return [[-10., -10.], [10., 10.], [0.1, 0.1]]
        elif function_name == FunctionNames.EASOM:
            return [[-100., -100.], [100., 100.], [0.1, 0.1]]
        if function_name == FunctionNames.CROSS_IN_TRAY:
            return [[-10., -10.], [10., 10.], [0.1, 0.1]]
        if function_name == FunctionNames.HOLDER:
            return [[-10., -10.], [10., 10.], [0.1, 0.1]]
        elif function_name == FunctionNames.MC_CORNIC:
            return [[-1.5, -3.], [4., 4.], [0.1, 0.1]]
        elif function_name == FunctionNames.SCHAFFER:
            return [[-100., -100.], [100., 100.], [0.1, 0.5]]
        elif function_name == FunctionNames.STYBLINSKI_TANG:
            return [[-5., 1.], [5., 2.], [0.1, 0.1]]
        else:
            return [[-5., -5.], [5., 5.], [0.1, 0.1]]


class FunctionNames:
    def __init__(self):
        pass

    ACKLEYS = "Ackley's"
    SPHERE = "Sphere"
    ROSENBROCK = "Rosenbrock"
    BEALES = "Beale's"
    GOLDSTEIN_PRICE = "Goldstein-Price"
    BOOTHS = "Booth's"
    BUKIN = "Bukin"
    MATYAS = "Matyas"
    LEVI = "Levi"
    EASOM = "Easom"
    CROSS_IN_TRAY = "Cross-in-tray"
    HOLDER = "Holder"
    MC_CORNIC = "McCornick"
    SCHAFFER = "Schaffer"
    STYBLINSKI_TANG = "Styblinski-Tang"
