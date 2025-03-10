"""
Module: fusion_logger_module

This module provides a centralized logging framework with configurable scopes and levels,
allowing applications to log messages with different severities and custom output destinations.
It integrates system metadata (such as hostname, process ID, and thread ID) into each log record
and supports dynamic log scoping.

Key Components:
----------------
1. FusionLogger:
   - A core logging class that handles logging at various levels (DEBUG, INFO, WARNING, CRITICAL).
   - Maintains system information (hostname, process ID, thread ID) and a set of file paths for logging output.
   - Supports setting a logging scope via the `begin_scope` and `end_scope` methods.
   - Uses a FusionLogProcessor to process log records and a FusionLogFormatter to format them.
   - The internal method `__log` creates a FusionLogRecord with the provided information and delegates
     processing to the FusionLogProcessor.
   - **Note:** The docstring for the `__log` method mentions that a NotImplementedError should be raised
     if the base class is used directly. However, the implementation does not raise this error. Could you
     clarify whether this behavior is intentional or if the method is expected to be overridden in subclasses?

2. FusionLoggerBuilder:
   - Implements a fluent builder pattern to simplify the configuration of FusionLogger instances.
   - Provides chainable methods to set the logger’s name, minimum logging level, custom formatter, and
     file output paths (both individually and in batches).
   - The `build` method returns a fully configured FusionLogger instance.
   - This builder allows users to configure the logger in a concise and readable manner.

Usage:
------
The module is designed to be integrated into applications requiring detailed logging functionality.
Users can either work directly with FusionLogger or use FusionLoggerBuilder for a more fluent configuration
process. The logging framework depends on other modules (.defs and .processors)
for log level definitions, record structures, formatting, and processing logic, and it leverages standard
libraries (os, socket, threading, time) to gather system metadata and support concurrency.
"""

import os
import socket
import threading
import time

from fusion_logger.defs import FusionLogLevel, FusionLogRecord
from fusion_logger.processors import FusionLogFormatter, FusionLogProcessor


class FusionLogger:
    """
    Central logging component with configurable scopes and levels.

    Attributes:
        name (str): Logger identification (default: class name)
        scope (str): Active logging context scope
        min_level (FusionLogLevel): Minimum output level for logs
        formatter (FusionLogFormatter): Log entry formatting component
    """

    def __init__(self):
        """
        Initializes the logger with system metadata and default values.
        """
        self.name: str = FusionLogger.__name__
        self.scope: str = ""
        self.min_level: FusionLogLevel = FusionLogLevel.INFO
        self.formatter: FusionLogFormatter = FusionLogFormatter("")
        self.processor: FusionLogProcessor = FusionLogProcessor()
        self.hostname: str = socket.gethostname()
        self.pid: int = os.getpid()
        self.tid: int = threading.current_thread().ident
        self.log_files: set = set()

    # Outer methods
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def debug(self, message: str, exception: Exception = None) -> None:
        """
        Logs a message at the DEBUG level.

        Args:
            message: The text message to log
            exception: Optional exception object (default: None)
        """
        self.__log(FusionLogLevel.DEBUG, message, exception)

    def info(self, message: str, exception: Exception = None) -> None:
        """
        Logs a message at the INFO level.

        Args:
            message: The text message to log
            exception: Optional exception object (default: None)
        """
        self.__log(FusionLogLevel.INFO, message, exception)

    def warning(self, message: str, exception: Exception = None) -> None:
        """
        Logs a message at the WARNING level.

        Args:
            message: The text message to log
            exception: Optional exception object (default: None)
        """
        self.__log(FusionLogLevel.WARNING, message, exception)

    def critical(self, message: str, exception: Exception = None) -> None:
        """
        Logs a message at the CRITICAL level.

        Args:
            message: The text message to log
            exception: Optional exception object (default: None)
        """
        self.__log(FusionLogLevel.CRITICAL, message, exception)

    def begin_scope(self, scope: str) -> None:
        """
        Activates a new logging context scope.

        Args:
            scope: Name of the new scope
        """
        self.scope = scope

    def end_scope(self, scope: str) -> None:
        """
        Ends the current logging context scope.

        Args:
            scope: Name of the scope to close (checks for consistency)
        """
        if self.scope == scope:
            self.scope = ""

    def set_min_level(self, min_level: FusionLogLevel) -> None:
        """
        Sets the minimum output level for logs.

        Args:
            min_level: New minimum level as a FusionLogLevel enum
        """
        self.min_level = min_level

    # Inner methods
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def __log(self, level: FusionLogLevel, message: str, exception: Exception):
        """
        Internal logging mechanism (must be implemented).

        Args:
            level: Desired log level
            message: Message to log
            exception: Optional exception reference
        """
        if self.__is_enabled(level):
            logging_record: FusionLogRecord = FusionLogRecord(
                logger=self,
                level=level,
                message=message,
                timestamp=time.time(),
                hostname=self.hostname,
                process_id=self.pid,
                thread_id=self.tid,
                exception=exception,
                files=self.log_files
            )
            self.processor.process_record(logging_record)

    def __is_enabled(self, level: FusionLogLevel) -> bool:
        """
        Checks if logging is enabled for the specified level.

        Args:
            level: Log level to check

        Returns:
            bool: True if logging is allowed, False otherwise
        """
        return level.value >= self.min_level.value


class FusionLoggerBuilder:
    """
    Fluent builder for configuring fusion_logger instances.

    Allows method chaining for easy logger creation.
    """

    def __init__(self):
        """
        Initializes the builder with a standard logger configuration.
        """
        self.__logger = FusionLogger()

    def set_name(self, name: str):
        """
        Sets the logger name.

        Args:
            name: Unique identifier for the logger

        Returns:
            FusionLoggerBuilder: Self-reference for method chaining
        """
        self.__logger.name = name
        return self

    def set_min_level(self, level: FusionLogLevel):
        """
        Configures the minimum log level.

        Args:
            level: Desired minimum level

        Returns:
            FusionLoggerBuilder: Self-reference for method chaining
        """
        self.__logger.min_level = level
        return self

    def set_formatter(self, fusion_formatter: FusionLogFormatter):
        """
        Sets a custom log formatter.

        Args:
            fusion_formatter: Formatter instance

        Returns:
            FusionLoggerBuilder: Self-reference for method chaining
        """
        self.__logger.formatter = fusion_formatter
        return self

    def write_to_file(self, path: str):
        """
        Adds a file path for logging output.

        Args:
            path: File path to write logs to

        Returns:
            FusionLoggerBuilder: Self-reference for method chaining
        """
        self.__logger.log_files.add(path)
        return self

    def write_to_files(self, *args: str):
        """
        Adds multiple file paths for logging output.

        Args:
            *args: Variable number of file paths

        Returns:
            FusionLoggerBuilder: Self-reference for method chaining
        """
        paths = list(args)
        for path in paths:
            self.__logger.log_files.add(path)
        return self

    def build(self):
        """
        Creates a fully configured logger instance.

        Returns:
            FusionLogger: Fully configured logger
        """
        return self.__logger
