import inspect
import os
import socket
import threading

from FusionLogLevel import FusionLogLevel
from FusionLogFormatter import FusionLogFormatter

class FusionLogger(object):
    """ TODO """

    def __init__(self):
        """ TODO """

        self.name: str = FusionLogger.__name__
        """ TODO """

        self.scope: str = ""
        """ TODO """

        self.min_level: FusionLogLevel = FusionLogLevel.Info
        """ TODO """

        self._formatter: FusionLogFormatter = FusionLogFormatter()
        """ TODO """

        self.__hostname: str = socket.gethostname()
        """ TODO """

        self.__pid: int = os.getpid()
        """ TODO """

        self.__tid: int = threading.current_thread().ident
        """ TODO """

    # Outer methods
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def debug(self, message: str, exception: Exception = None) -> None:
        """ TODO """
        self.__log(FusionLogLevel.Debug, message, exception)

    def info(self, message: str, exception: Exception = None) -> None:
        """ TODO """
        self.__log(FusionLogLevel.Info, message, exception)

    def warning(self, message: str, exception: Exception = None) -> None:
        """ TODO """
        self.__log(FusionLogLevel.Warning, message, exception)

    def critical(self, message: str, exception: Exception = None) -> None:
        """ TODO """
        self.__log(FusionLogLevel.Critical, message, exception)

    def begin_scope(self, scope: str) -> None:
        """ TODO """
        pass

    def end_scope(self, scope: str) -> None:
        """ TODO """
        pass

    def set_min_level(self, min_level: FusionLogLevel) -> None:
        self.min_level = min_level

    # Inner methods
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def __log(self, level: FusionLogLevel, message: str, exception: Exception):
        """ TODO """
        pass

    def __is_enabled (self, level: FusionLogLevel) -> bool:
        """ TODO """
        pass

class FusionLoggerBuilder(object):
    """ TODO """

    def __init__(self):
        """ TODO """
        self.__logger = FusionLogger()

    def set_name(self, name: str):
        """ TODO """
        self.__logger.name = name
        return self

    def set_min_level(self, level: FusionLogLevel):
        """ TODO """
        self.__logger.min_level = level
        return self

    def set_formatter(self, formatter: FusionLogFormatter):
        """ TODO """
        self.__logger.Formatter = formatter
        return self

    def build(self):
        """ TODO """
        return self.__logger


def caller_info(skip=2):
    """Get the name of a caller in the format module.class.method.
    Copied from: https://gist.github.com/techtonik/2151727
    :arguments:
        - skip (integer): Specifies how many levels of stack
                          to skip while getting caller name.
                          skip=1 means "who calls me",
                          skip=2 "who calls my caller" etc.
    :returns:
        - package (string): caller package.
        - module (string): caller module.
    """
    stack = inspect.stack()
    start = 0 + skip
    if len(stack) < start + 1:
        return ''
    parentframe = stack[start][0]

    # module and packagename.
    module: str = ""
    module_info = inspect.getmodule(parentframe)
    if module_info:
        module = module_info.__name__

    # Remove reference to frame
    # See: https://docs.python.org/3/library/inspect.html#the-interpreter-stack
    del parentframe
    return module


def deepened():
    print(caller_info())


if __name__ == "__main__":
    deepened()
