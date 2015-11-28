import sys

try:
    from PyQt5.QtGui import QColor
except ImportError as error:
    print error.message
    print "PyQt5 is necessary"
    sys.exit("Not all the requirements are fulfilled")


class TextAreaLogger(object):
    """Logger for QTextArea class - singleton patter"""
    def __init__(self):
        pass

    """Output stream"""
    _out = None
    """Only one instance of the class"""
    _instance = None

    class _Logger:
        def __init__(self, out):
            self.out = out

        def log(self, text, color=None):
            if color:
                self.set_text_color(color)
            if self.out:
                self.out.append(text)
            else:
                print text
            if color:
                self.reset_text_color()

        def set_text_color(self, color):
            if self.out:
                self.out.setTextColor(QColor(color))

        def reset_text_color(self):
            if self.out:
                self.out.setTextColor(QColor("black"))

    @staticmethod
    def get_instance():
        """Get instance of Logger"""
        if not TextAreaLogger._instance:
            TextAreaLogger._instance = TextAreaLogger._Logger(TextAreaLogger._out)
        return TextAreaLogger._instance

    @staticmethod
    def set_output_stream(out):
        """Set output stream for logging"""
        TextAreaLogger._out = out


class ConsoleLogger(TextAreaLogger):
    class _Logger(TextAreaLogger._Logger):
        def log(self, text, color=None):
            print "Console Logger: " + text
            TextAreaLogger._Logger.log(self, text, color)

    @staticmethod
    def get_instance():
        """Get instance of Logger"""
        if not ConsoleLogger._instance:
            ConsoleLogger._instance = ConsoleLogger._Logger(ConsoleLogger._out)
        return ConsoleLogger._instance


class ResultLogger(TextAreaLogger):
    class _Logger(TextAreaLogger._Logger):
        def log(self, text, color=None):
            print "Result Logger: " + text
            TextAreaLogger._Logger.log(self, text, color)

    @staticmethod
    def get_instance():
        """Get instance of Logger"""
        if not ResultLogger._instance:
            ResultLogger._instance = ResultLogger._Logger(ResultLogger._out)
        return ResultLogger._instance
