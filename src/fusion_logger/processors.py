"""
Module: processors
---------------
This module provides components for formatting and processing log records. It includes functionality to
parse a log message template into tokens, format log records
according to that template, and process the resulting messages by outputting them to the console and files.

Key Components:
---------------
1. FusionLogFormatter: \n
   - Formats log records based on a specified template.
   - On initialization, it parses the template string into a list of tokens using the `parse_template` function.
   - Supports an optional custom datetime format for timestamp formatting.
   - The `apply_template` method applies the sequence of tokens to a FusionLogRecord to produce a formatted log message.

2. parse_template (Function): \n
   - Parses a template string containing placeholders (delimited by curly braces) into a list of tokens.
   - Converts text segments into LiteralToken objects and placeholder segments into FormatToken objects.

3. SingletonMeta (Metaclass): \n
   - Implements a thread-safe Singleton design pattern.
   - Ensures that any class using this metaclass (such as FusionLogProcessor) has only one instance.
   - Uses a locking mechanism to manage concurrent instance creation.

4. FusionLogProcessor: \n
   - Processes log records using a singleton instance (guaranteed by SingletonMeta).
   - Maintains a thread-safe message queue for log records.
   - The static method `process_record` formats a log record using the associated formatter, prints the
   formatted output, and writes it to any designated log files.

Usage:
------
This module is intended to integrate with the larger logging system, where log records (FusionLogRecord)
are created, formatted, and processed. Developers can define custom formatting templates to control log output,
and the FusionLogProcessor ensures that log messages are handled in a thread-safe, singleton manner.

"""

import threading

from .defs import FusionLogRecord, Token, LiteralToken, FormatToken


class FusionLogFormatter:
    """
    Formats log records based on a given template.

    Attributes:
        tokens (list[Token]): List of tokens parsed from the template.
        datetime_format (str): Optional format for datetime fields.
    """

    def __init__(self, template: str, datetime_format: str = None):
        """
        Initializes the formatter with a template and optional datetime format.

        Args:
            template (str): Template string containing placeholders for log attributes.
            datetime_format (str): Optional format for datetime fields (default: None).
        """
        self.tokens: list[Token] = parse_template(template)
        self.datetime_format = datetime_format

    def apply_template(self, record: FusionLogRecord) -> str:
        """
        Applies the template to a log record, returning the formatted string.

        Args:
            record (FusionLogRecord): The log entry to be formatted.

        Returns:
            str: The formatted log message.
        """
        out: str = ""
        for token in self.tokens:
            out = token.apply(record, out)
        return out


def parse_template(template: str) -> list:
    """
    Parses a template string into a list of tokens.

    Args:
        template (str): Template string containing placeholders for log attributes.

    Returns:
        list[Token]: List of tokens representing the template.
    """
    tokens: list = list()
    position: int = 0
    while position < len(template):
        start: int = template.find("{", position)

        # Remaining text is a literal token
        if start == -1:
            tokens.append(LiteralToken(template[position:]))
            break

        # Text before format identifier is a literal token
        if start > position:
            tokens.append(LiteralToken(template[position:start]))

        end: int = template.find("}", start)

        # If no end is found, treat the rest as a literal token
        if end == -1:
            tokens.append(LiteralToken(template[start:]))
            break

        key = template[start + 1:end]
        tokens.append(FormatToken(key))
        position = end + 1
    return tokens


class SingletonMeta(type):
    """
    Metaclass implementing a thread-safe Singleton pattern.

    Attributes:
        _instances (dict): Stores singleton instances of created classes.
        _lock (threading.Lock): Lock for thread-safe instance creation.
    """

    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        """
        Creates or returns an existing class instance.
        Thread-safe implementation using a lock.

        Args:
            *args: Variable positional arguments.
            **kwargs: Variable keyword arguments.

        Returns:
            object: The single instance of the class.
        """
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class FusionLogProcessor(metaclass=SingletonMeta):
    """
    Central processor for log records with a Singleton implementation.
    Manages a processing queue and a background thread.
    """

    def __init__(self) -> None:
        """
        Initializes the processor with an empty queue.
        """
        # self._queue = Queue()

    @staticmethod
    def process_record(record: FusionLogRecord) -> None:
        """
        Processes individual log records (must be overridden).

        Args:
            record (FusionLogRecord): Log entry to be processed.

        Returns:
            str: Formatted output string.
        """
        out: str = record.logger.formatter.apply_template(record)
        print(out)
        for file in record.files:
            with open(file, "a", encoding="utf-8") as opened_file:
                opened_file.write(out)
                opened_file.write("\n")
