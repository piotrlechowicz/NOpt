class PredefinedFunctions:
    "todo: encode it"
    @staticmethod
    def get_function(function_name):
        if function_name == FunctionNames.ACKLEYS:
            pass
        elif function_name == FunctionNames.SPHERE:
            return "x^2 + y^2"
        if function_name == FunctionNames.ROSENBROCK:
            pass
        elif function_name == FunctionNames.BEALES:
            pass
        if function_name == FunctionNames.GOLDSTEIN_PRICE:
            pass
        elif function_name == FunctionNames.BOOTHS:
            pass
        if function_name == FunctionNames.BOOKIN:
            pass
        elif function_name == FunctionNames.MATYAS:
            pass
        if function_name == FunctionNames.LEVI:
            pass
        elif function_name == FunctionNames.EASOM:
            pass
        if function_name == FunctionNames.CROSS_IN_TRAY:
            pass
        elif function_name == FunctionNames.EGGHOLDER:
            pass
        if function_name == FunctionNames.HOLDER:
            pass
        elif function_name == FunctionNames.MC_CORNIC:
            pass
        elif function_name == FunctionNames.SCHAFFER:
            pass
        elif function_name == FunctionNames.STYBLINSKI_TANG:
            pass
        elif function_name == FunctionNames.SIMIONESCU:
            pass

    @staticmethod
    def get_properties(function_name):
        if function_name == FunctionNames.ACKLEYS:
            pass
        elif function_name == FunctionNames.SPHERE:
            return [[-5., -5.], [5., 5.], [0.1, 0.1]]
        if function_name == FunctionNames.ROSENBROCK:
            pass
        elif function_name == FunctionNames.BEALES:
            pass
        if function_name == FunctionNames.GOLDSTEIN_PRICE:
            pass
        elif function_name == FunctionNames.BOOTHS:
            pass
        if function_name == FunctionNames.BOOKIN:
            pass
        elif function_name == FunctionNames.MATYAS:
            pass
        if function_name == FunctionNames.LEVI:
            pass
        elif function_name == FunctionNames.EASOM:
            pass
        if function_name == FunctionNames.CROSS_IN_TRAY:
            pass
        elif function_name == FunctionNames.EGGHOLDER:
            pass
        if function_name == FunctionNames.HOLDER:
            pass
        elif function_name == FunctionNames.MC_CORNIC:
            pass
        elif function_name == FunctionNames.SCHAFFER:
            pass
        elif function_name == FunctionNames.STYBLINSKI_TANG:
            pass
        elif function_name == FunctionNames.SIMIONESCU:
            pass


class FunctionNames:
     ACKLEYS = "Ackley's"
     SPHERE = "Sphere"
     ROSENBROCK = "Rosenbrock"
     BEALES = "Beale's"
     GOLDSTEIN_PRICE = "Goldstein-price"
     BOOTHS = "Booth's"
     BOOKIN = "Bookin"
     MATYAS = "Matyas"
     LEVI = "Levi"
     EASOM = "Easom"
     CROSS_IN_TRAY = "Cross-in-tray"
     EGGHOLDER = "Eggholder"
     HOLDER = "Holder"
     MC_CORNIC = "McCornic"
     SCHAFFER = "Schaffer"
     STYBLINSKI_TANG = "Styblinski-Tang"
     SIMIONESCU = "Simionescu"


