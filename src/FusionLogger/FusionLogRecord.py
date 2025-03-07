from dataclasses import dataclass

from FusionLogger.FusionLogger import FusionLogger
from FusionLogger.FusionLogLevel import FusionLogLevel


@dataclass
class FusionLogRecord(object):
    logger: FusionLogger
    level: FusionLogLevel
    message: str
    timestamp: float