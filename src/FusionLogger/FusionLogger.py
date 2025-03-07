import inspect
from types import FrameType
from typing import cast

from FusionLogLevel import FusionLogLevel


class FusionLogger(object):

    def __init__(self):
        pass

    def __str__(self):
        pass

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Fundamental methods
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def Debug(self, message):
        pass

    def Info(self, message):
        pass

    def Warning(self, message: str, exception: Exception):
        pass

    def Critical(self, message: str, exception: Exception):
        pass

    def BeginScope(self, scope: str):
        pass

    def EndScope(self, scope: str):
        pass

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Inner methods
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def __Log(self, level: FusionLogLevel, message: str, exception: Exception):
        pass

    @staticmethod
    def demo_the_caller_name() -> tuple[str, str]:
        """Return the calling function's name."""
        # Ref: https://stackoverflow.com/a/57712700/
        method: str = cast(FrameType, cast(FrameType, inspect.currentframe()).f_back).f_code.co_name
        clazz: str = cast(FrameType, cast(FrameType, inspect.currentframe()).f_back).f_code.co_qualname
        return method, clazz

def deepened():
    (method, clazz) =FusionLogger.demo_the_caller_name()
    print(clazz)
    print(method)

if __name__ == "__main__":
    deepened()


