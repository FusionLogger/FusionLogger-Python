from dataclasses import dataclass

from FusionLogger.FusionLogLevel import FusionLogLevel
from FusionLogger.FusionLogger import FusionLogger


@dataclass
class FusionLogRecord(object):
    logger: FusionLogger
    level: FusionLogLevel
    message: str
    timestamp: float
    hostname: str
    process_id : int
    thread_id: int

