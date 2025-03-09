import inspect
import sys
from types import FrameType
from typing import cast

from FusionLogLevel import FusionLogLevel
from FusionLogFormatter import FusionLogFormatter


class FusionLogger(object):

    def __init__(self):
        self.MinLogLevel = FusionLogLevel.Info
        self.Formatter = FusionLogFormatter()

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Fundamental methods
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def debug(self, message):
        pass

    def info(self, message):
        pass

    def warning(self, message: str, exception: Exception):
        pass

    def critical(self, message: str, exception: Exception):
        pass

    def begin_scope(self, scope: str):
        pass

    def end_scope(self, scope: str):
        pass

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Inner methods
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def __log(self, level: FusionLogLevel, message: str, exception: Exception):
        """

        """

        # Erstellung des
        pass


class FusionLoggerBuilder(object):
    def __init__(self):
        self.Logger = FusionLogger()

    def set_name(self, name: str):
        self.Logger.Name = name
        return self

    def set_loglevel(self, level: FusionLogLevel):
        self.Logger.MinLogLevel = level
        return self

    def set_formatter(self, formatter: FusionLogFormatter):
        self.Logger.Formatter = formatter
        return self

    def build(self):
        return self.Logger


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
    package: str = ""
    module: str = ""
    module_info = inspect.getmodule(parentframe)
    if module_info:
        mod = module_info.__name__.split('.')
        package: str = mod[0]
        module: str = mod[1]

    # Remove reference to frame
    # See: https://docs.python.org/3/library/inspect.html#the-interpreter-stack
    del parentframe
    return package, module


def deepened():
    FusionLogger.module_from_stack()


if __name__ == "__main__":
    deepened()
