"""
Module Description: defs

This module implements structures that enable structured and thread-safe log entries. It provides two central components:

- **FusionLogLevel (Enum):**
  Defines four severity levels for log messages. These severity levels are:
    -  **DEBUG (0):** For detailed debug information during development, such as variable states and execution traces.
    -  **INFO (1):** For general system information, such as successful transactions and system startup/shutdown events.
    -  **WARNING (2):** To indicate potential problem areas, such as unexpected but manageable conditions.
    -  **CRITICAL (3):** For severe system errors, e.g., unmanageable exceptions and data loss.

- **FusionLogRecord (Data Class):**
  A data container encapsulating all relevant metadata of a log entry. It includes:
    -  **logger:** Reference to the logger (FusionLogger) that created the entry.
    -  **level:** The severity level of the event, based on FusionLogLevel.
    -  **message:** The unformatted original message.
    -  **timestamp:** The creation time as a Unix timestamp (UTC).
    -  **hostname:** The hostname of the originating system.
    -  **process_id:** The process ID of the generating process.
    -  **thread_id:** The thread ID of the generating thread.
"""

from dataclasses import dataclass
from enum import Enum

from .core import FusionLogger


class FusionLogLevel(Enum):
    """
    Definiert die Schweregrade für Loggingmeldungen in einem mehrstufigen Logging-System.

    Attributes:
        DEBUG: Niedrigste Stufe für Entwicklerdiagnosen
        INFO: Allgemeine Systeminformationen
        WARNING: Potenzielle Probleme
        CRITICAL: Kritische Systemfehler
    """

    DEBUG = 0
    """
    Verwendet für detaillierte Debug-Informationen während der Entwicklung.

    Typische Anwendungen:
        - Variablenzustände
        - Ablaufverfolgung
        - Temporäre Diagnoseausgaben
    """

    INFO = 1
    """
    Beschreibt reguläre Systemoperationen.

    Wichtige Ereignisse:
        - Erfolgreiche Transaktionen
        - Systemstart/Shutdown
        - Konfigurationsänderungen
    """

    WARNING = 2
    """
    Kennzeichnet potenzielle Problemstellen.

    Anwendungsfälle:
        - Unerwartete aber behandelbare Zustände
        - Deprecation-Hinweise
        - Ressourcenengpässe
    """

    CRITICAL = 3
    """
    Dokumentiert schwerwiegende Systemfehler.

    Wird verwendet bei:
        - Nicht behandelbaren Ausnahmen
        - Datenverlusten
        - Kritischen Abhängigkeitsfehlern
    """


@dataclass
class FusionLogRecord(object):
    """
    Datencontainer für strukturierte Logginginformationen.

    Kapselt alle relevanten Metadaten und Inhalte eines Logeintrags
    in einem threadsicheren Format.

    Attributes:
        logger (FusionLogger): Quell-Logger-Instanz
        level (FusionLogLevel): Schweregrad des Ereignisses
        message (str): Rohtextnachricht des Logeintrags
        timestamp (float): Unix-Zeitstempel der Erstellung
        hostname (str): Rechnername des Ursprungssystems
        process_id (int): Prozesskennung des Erzeugers
        thread_id (int): Threadkennung des Erzeugers
    """

    logger: FusionLogger
    """
    Referenz auf den erzeugenden Logger (automatisch gesetzt)

    """

    level: FusionLogLevel
    """
    Schweregrad des Ereignisses (DEBUG/INFO/WARNING/CRITICAL)
    """

    message: str
    """
    Unformatierte Originalnachricht des Logeintrags
    """

    timestamp: float
    """
    Erstellungszeitpunkt als Unix-Zeitstempel (UTC)
    """

    hostname: str
    """
    Hostname des erzeugenden Systems (automatisch gesetzt)
    """

    process_id: int
    """
    PID des erzeugenden Prozesses (automatisch gesetzt)
    """

    thread_id: int
    """
    TID des erzeugenden Threads (automatisch gesetzt)
    """
