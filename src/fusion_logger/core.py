"""
Module: core
---------------------

This module implements a flexible and configurable logging component for Python applications.
It provides two main classes:

1. fusion_logger:
   - The central logging component that supports configurable scopes and log levels.
   - Automatically gathers system metadata such as hostname, process ID, and current thread ID.
   - Supports logging methods at various levels (debug, info, warning, critical) by creating
     FusionLogRecord instances enriched with metadata.
   - Delegates log record processing to a FusionLogProcessor, and formats log entries using a
     FusionLogFormatter.
   - Allows dynamic configuration of the current logging scope and minimum log level.

2. FusionLoggerBuilder:
   - Implements a fluent builder pattern to facilitate the creation and configuration of fusion_logger
     instances.
   - Provides chainable methods for setting the logger name, minimum log level, and custom formatter.
   - Finalizes and returns a fully configured fusion_logger instance using the build() method.

Dependencies:
    - os, socket, threading, and time from the standard library.
    - FusionLogLevel and FusionLogRecord from the local 'defs' module.
    - FusionLogFormatter and FusionLogProcessor from the local 'processors' module.

Usage:
    Use fusion_logger for logging messages with rich contextual metadata and configurable behavior.
    For ease of configuration, instantiate a FusionLoggerBuilder to set up the logger with the desired
    properties and then build the logger instance.
"""

import os
import socket
import threading
import time

from fusion_logger.defs import FusionLogLevel, FusionLogRecord
from fusion_logger.processors import FusionLogFormatter, FusionLogProcessor


class FusionLogger(object):
    """
    Zentrale Logging-Komponente mit konfigurierbaren Scopes und Leveln.

    Attributes:
        name (str): Logger-Identifikation (Standard: Klassenname)
        scope (str): Aktiver Logging-Kontextbereich
        min_level (FusionLogLevel): Minimale Ausgabestufe für Logs
        formatter (FusionLogFormatter): Formatierungskomponente für Logeinträge
    """

    def __init__(self):
        """
        Initialisiert Logger mit Systemmetadaten und Defaultwerten.
        """
        self.name: str = FusionLogger.__name__
        self.scope: str = ""
        self.min_level: FusionLogLevel = FusionLogLevel.INFO
        self.formatter: FusionLogFormatter = FusionLogFormatter("")
        self.processor: FusionLogProcessor = FusionLogProcessor()
        self.hostname: str = socket.gethostname()
        self.pid: int = os.getpid()
        self.tid: int = threading.current_thread().ident

    # Outer methods
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def debug(self, message: str, exception: Exception = None) -> None:
        """
        Loggt eine Nachricht auf DEBUG-Level.

        Args:
            message: Zu loggende Textnachricht
            exception: Optionales Exception-Objekt (Standard: None)
        """
        self.__log(FusionLogLevel.DEBUG, message, exception)

    def info(self, message: str, exception: Exception = None) -> None:
        """
        Loggt eine Nachricht auf INFO-Level.

        Args:
            message: Zu loggende Textnachricht
            exception: Optionales Exception-Objekt (Standard: None)
        """
        self.__log(FusionLogLevel.INFO, message, exception)

    def warning(self, message: str, exception: Exception = None) -> None:
        """
        Loggt eine Nachricht auf WARNING-Level.

        Args:
            message: Zu loggende Textnachricht
            exception: Optionales Exception-Objekt (Standard: None)
        """
        self.__log(FusionLogLevel.WARNING, message, exception)

    def critical(self, message: str, exception: Exception = None) -> None:
        """
        Loggt eine Nachricht auf CRITICAL-Level.

        Args:
            message: Zu loggende Textnachricht
            exception: Optionales Exception-Objekt (Standard: None)
        """
        self.__log(FusionLogLevel.CRITICAL, message, exception)

    def begin_scope(self, scope: str) -> None:
        """
        Aktiviert einen neuen Logging-Kontextbereich.

        Args:
            scope: Name des neuen Kontextbereichs
        """
        self.scope = scope

    def end_scope(self, scope: str) -> None:
        """
        Beendet den aktuellen Logging-Kontextbereich.

        Args:
            scope: Name des zu schließenden Bereichs (Prüfung auf Konsistenz)
        """
        if self.scope == scope:
            self.scope = ""

    def set_min_level(self, min_level: FusionLogLevel) -> None:
        """
        Setzt die minimale Ausgabestufe für Logs.

        Args:
            min_level: Neue Mindeststufe als FusionLogLevel-Enum
        """
        self.min_level = min_level

    # Inner methods
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def __log(self, level: FusionLogLevel, message: str, exception: Exception):
        """
        Interner Logging-Mechanismus (muss implementiert werden).

        Args:
            level: Gewünschtes Log-Level
            message: Zu loggende Nachricht
            exception: Optionale Exception-Referenz

        Raises:
            NotImplementedError: Bei direkter Verwendung der Basisklasse
        """
        logging_record: FusionLogRecord = FusionLogRecord(
            logger=self,
            level=level,
            message=message,
            timestamp=time.time(),
            hostname=self.hostname,
            process_id=self.pid,
            thread_id=self.tid,
        )
        self.processor.process_record(logging_record)

    def __is_enabled(self, level: FusionLogLevel) -> bool:
        """
        Prüft, ob Logging für angegebenes Level aktiviert ist.

        Args:
            level: Zu prüfendes Log-Level

        Returns:
            bool: True wenn Logging erlaubt, sonst False
        """
        return level.value >= self.min_level.value


class FusionLoggerBuilder(object):
    """
    Fluent Builder für die Konfiguration von fusion_logger-Instanzen.

    Ermöglicht method chaining für einfache Logger-Erstellung.
    """

    def __init__(self):
        """
        Initialisiert Builder mit Standard-Loggerkonfiguration.
        """
        self.__logger = FusionLogger()

    def set_name(self, name: str):
        """
        Setzt den Logger-Namen.

        Args:
            name: Eindeutiger Identifikator für den Logger

        Returns:
            FusionLoggerBuilder: Selbstreferenz für Method Chaining
        """
        self.__logger.name = name
        return self

    def set_min_level(self, level: FusionLogLevel):
        """
        Konfiguriert die minimale Log-Stufe.

        Args:
            level: Gewünschte Mindeststufe

        Returns:
            FusionLoggerBuilder: Selbstreferenz für Method Chaining
        """
        self.__logger.min_level = level
        return self

    def set_formatter(self, formatter: FusionLogFormatter):
        """
        Setzt benutzerdefinierten Log-Formatter.

        Args:
            formatter: Formatter-Instanz

        Returns:
            FusionLoggerBuilder: Selbstreferenz für Method Chaining
        """
        self.__logger.formatter = formatter
        return self

    def build(self):
        """
        Erzeugt final konfigurierte Logger-Instanz.

        Returns:
            FusionLogger: Vollständig konfigurierter Logger
        """
        return self.__logger


if __name__ == "__main__":
    formatter = FusionLogFormatter("[{LEVEL}] {TIMESTAMP} [{NAME}] {MESSAGE}")
    logger = FusionLoggerBuilder().set_formatter(formatter).build()
    logger.debug("Hallo")
    logger.info("Hallo")
    logger.warning("Hallo")
    logger.critical("Hallo")
