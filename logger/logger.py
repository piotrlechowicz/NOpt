import sys

try:
    from PyQt5.QtGui import QColor
except ImportError as error:
    print error.message
    print "PyQt5 is necessary"
    sys.exit("Not all the requirements are fulfilled")

from enum import Enum


class LoggerLevel(Enum):
    NORMAL = 1
    ADDITIONAL = 2
    INFO = 3
    DEBUG = 4
    WARN = 5
    ERROR = 6

    @staticmethod
    def get_logger_color(log_level=NORMAL):
        return {LoggerLevel.NORMAL: 'black',
                LoggerLevel.ADDITIONAL: 'gray',
                LoggerLevel.INFO: 'blue',
                LoggerLevel.DEBUG: 'green',
                LoggerLevel.WARN: 'orange',
                LoggerLevel.ERROR: 'red'}.get(log_level, 'black')


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

        def log(self, text, logger_level=None):
            if logger_level:
                self.set_text_color(logger_level)
            if self.out:
                self.out.append(text)
            else:
                print text
            if logger_level:
                self.reset_text_color()

        def set_text_color(self, logger_level):
            if self.out:
                color = LoggerLevel.get_logger_color(logger_level)
                self.out.setTextColor(QColor(color))

        def reset_text_color(self):
            if self.out:
                color = LoggerLevel.get_logger_color(LoggerLevel.NORMAL)
                self.out.setTextColor(QColor(color))

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
        def log(self, text, logger_level=None):
            print "Console Logger: " + text
            TextAreaLogger._Logger.log(self, text, logger_level)

    @staticmethod
    def get_instance():
        """Get instance of Logger"""
        if not ConsoleLogger._instance:
            ConsoleLogger._instance = ConsoleLogger._Logger(ConsoleLogger._out)
        return ConsoleLogger._instance


class ResultLogger(TextAreaLogger):
    class _Logger(TextAreaLogger._Logger):
        def log(self, text, logger_level=None):
            print "Result Logger: " + text
            TextAreaLogger._Logger.log(self, text, logger_level)

    @staticmethod
    def get_instance():
        """Get instance of Logger"""
        if not ResultLogger._instance:
            ResultLogger._instance = ResultLogger._Logger(ResultLogger._out)
        return ResultLogger._instance
