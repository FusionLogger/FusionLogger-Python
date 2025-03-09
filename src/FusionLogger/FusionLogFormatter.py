from FusionLogRecord import FusionLogRecord


class FusionLogFormatter(object):
    def __init__(self):
        pass

    def format(self, record: FusionLogRecord) -> str:
        return f"Formatted: {record.message}"
