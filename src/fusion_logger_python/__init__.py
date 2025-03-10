"""
FusionLogger-Python Package

This package provides the core components of the FusionLogger-Python logging framework. It enables
centralized logging with configurable log levels, dynamic scopes, and flexible, token-based formatting.
The package includes the following main components:

  - FusionLogger: The central logging class for creating and processing log messages.
  - FusionLoggerBuilder: A fluent builder for convenient configuration of FusionLogger instances.
  - FusionLogRecord: A structured data container for log entries, encapsulating all relevant metadata.
  - FusionLogLevel: An enumeration defining the available logging levels (DEBUG, INFO, WARNING, CRITICAL).
  - FusionLogFormatter: A formatter that applies custom templates to log records using tokens.
  - FusionLogProcessor: A processor for handling log output to various destinations (console and files).

These components work together to provide a high-performance, configurable logging solution for Python applications.
"""

from .core import FusionLogger, FusionLoggerBuilder
from .defs import FusionLogLevel, FusionLogRecord
from .processors import FusionLogFormatter, FusionLogProcessor

__all__ = [
    'FusionLogger',
    'FusionLogRecord',
    'FusionLogLevel',
    'FusionLogFormatter',
    'FusionLoggerBuilder',
    'FusionLogProcessor',
]
