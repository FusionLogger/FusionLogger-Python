"""
Module: defs
---------------
This module defines core constructs for the logging system, including severity levels,
a structured log record, and token classes for dynamic log formatting. It is designed
to encapsulate both the data structure for log entries and the mechanisms to transform
these entries into formatted strings.

Key Components:
---------------
1. FusionLogLevel (Enum): \n
   - Enumerates the logging severity levels: DEBUG, INFO, WARNING, and CRITICAL.
   - Each level is associated with an integer value to determine its hierarchy.
   - Detailed docstrings explain the intended usage and examples for each level.

2. FusionLogRecord (Data Class): \n
   - Serves as a structured container for log entries.
   - Encapsulates metadata such as the logger instance, log level, raw message,
     timestamp (in Unix format), hostname, process ID, thread ID, an optional exception,
     and a set of file paths where the log may be written.
   - Designed for thread-safe usage when handling log records.

3. Token (Abstract Base Class): \n
   - Acts as a base for tokens used in log formatting.
   - Defines the method `apply` which should be overridden in derived classes to
     manipulate a log record and build a formatted log string.

4. LiteralToken (Subclass of Token): \n
   - Implements a token that appends a fixed literal string to the formatted log output.
   - Primarily used for inserting static text into log formats.

5. FormatToken (Subclass of Token): \n
   - Processes dynamic placeholders by extracting corresponding attributes from a log record.
   - Supports tokens for logger name, scope, timestamp (with support for custom date-time formats),
     level (abbreviated to the first four characters), hostname, message, process ID, and thread ID.
   - Falls back to a default value ("UNKNOWN_FORMAT") if an unrecognized key is provided.

Usage:
------
This module is intended to work in tandem with the rest of the logging system. Log entries are
first encapsulated in a FusionLogRecord, then transformed into a formatted string via a series of
tokens (LiteralToken and FormatToken) defined here. The design supports extensibility for creating
additional token types if further customization is needed.
"""

import abc
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .core import FusionLogger  # Only for type checking


class FusionLogLevel(Enum):
    """
    Enumerates the severity levels for log messages.

    Attributes:
        DEBUG: Lowest level for development diagnostics
        INFO: General system operations
        WARNING: Potential issues requiring attention
        CRITICAL: Critical system failures
    """

    DEBUG = 0
    """
    Detailed debug information, such as:
        - Variable states
        - Execution tracing
        - Temporary diagnostic outputs
    """

    INFO = 1
    """
    Regular system operations, including:
        - Successful transactions
        - System startup and shutdown
        - Configuration changes
    """

    WARNING = 2
    """
    Warns about potential but manageable issues, such as:
        - Unexpected states
        - Deprecation notices
        - Resource bottlenecks
    """

    CRITICAL = 3
    """
    Indicates severe errors involving:
        - Unhandled exceptions
        - Data loss
        - Critical dependency failures
    """


@dataclass
class FusionLogRecord:
    """
    Structured data container for log entries.

    Encapsulates all relevant metadata of a log entry in a thread-safe format.

    Attributes:
        logger (FusionLogger): Reference to the logger instance that created the entry.
        level (FusionLogLevel): Severity level of the log event.
        message (str): The raw log message.
        timestamp (float): Unix timestamp when the log entry was created.
        hostname (str): Name of the system where the log entry was generated.
        process_id (int): Process ID of the creating process.
        thread_id (int): Thread ID of the creating thread.
        exception (Exception): Optional exception passed during logging.
        files (set[str]): Files where the message is written.
    """

    logger: "FusionLogger"
    """
    Reference to the logger that created the entry.
    """

    level: FusionLogLevel
    """
    Severity level of the log event, e.g., DEBUG, INFO, WARNING, or CRITICAL.
    """

    message: str
    """
    The original, unformatted message of the log entry.
    """

    timestamp: float
    """
    Creation time of the log entry as a Unix timestamp (UTC).
    """

    hostname: str
    """
    Name of the system where the log entry was generated.
    """

    process_id: int
    """
    Process ID of the process that created the entry.
    """

    thread_id: int
    """
    Thread ID of the thread that created the entry.
    """

    exception: Exception
    """
    Optional exception passed during logging.
    """

    files: set[str]
    """
    Files where the message is written.
    """


class Token:
    """
    Abstract base class for tokens used in log formatting.

    Provides a placeholder for applying tokens to log records.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def apply(self, record: FusionLogRecord, built: str) -> str:
        """
        Applies the token to the given log record and builds the formatted string.

        Args:
            record (FusionLogRecord): The log entry to be formatted.
            built (str): The string built so far.

        Returns:
            str: The updated string after applying the token.
        """
        pass  # This method serves as a placeholder and should be implemented in derived classes.


class LiteralToken(Token):
    """
    Token that appends a literal string without further formatting.
    """

    def __init__(self, literal: str):
        """
        Initializes a LiteralToken with the given literal string.

        Args:
            literal (str): The literal string to be appended.
        """
        self.literal = literal

    def apply(self, record: FusionLogRecord, built: str) -> str:
        """
        Appends the literal string to the built string.

        Args:
            record (FusionLogRecord): The log entry (not used here).
            built (str): The string built so far.

        Returns:
            str: The string extended with the literal string.
        """
        built += self.literal
        return built


class FormatToken(Token):
    """
    Token that formats placeholders by extracting relevant attributes from a log record.
    """

    _logger_name_format: str = "NAME"
    _logger_scope_format: str = "SCOPE"
    _level_format: str = "LEVEL"
    _hostname_format: str = "HOSTNAME"
    _message_format: str = "MESSAGE"
    _timestamp_format: str = "TIMESTAMP"
    _process_id_format: str = "PID"
    _thread_id_format: str = "TID"

    def __init__(self, key: str):
        """
        Initializes a FormatToken with the specified key.

        Args:
            key (str): The key indicating which attribute to format from the log record.
        """
        self.key = key

    def apply(self, record: FusionLogRecord, built: str) -> str:
        """
        Applies the FormatToken by appending the corresponding attribute value from the log record to the built string.

        Args:
            record (FusionLogRecord): The log entry with all relevant metadata.
            built (str): The string built so far.

        Returns:
            str: The updated string after applying the FormatToken.
        """
        # Check the key and append the corresponding value.
        if self.key == self._logger_name_format:
            built += record.logger.name

        elif self.key == self._logger_scope_format:
            built += record.logger.scope

        elif self.key == self._timestamp_format:
            if record.logger.formatter.datetime_format is None:
                built += datetime.fromtimestamp(record.timestamp).strftime("%Y-%m-%d %H:%M:%S")
            else:
                built += datetime.fromtimestamp(record.timestamp).strftime(record.logger.formatter.datetime_format)

        elif self.key == self._level_format:
            built += record.level.name[:4]

        elif self.key == self._hostname_format:
            built += record.hostname

        elif self.key == self._message_format:
            built += record.message

        elif self.key == self._process_id_format:
            built += str(record.process_id)

        elif self.key == self._thread_id_format:
            built += str(record.thread_id)

        else:
            built += "UNKNOWN_FORMAT"

        return built
