"""
Module: defs
-------------------

Dieses Modul stellt grundlegende Definitionen für ein mehrstufiges Logging-System bereit.
Es enthält zwei Hauptkomponenten:

1. FusionLogLevel (Enum):
   Definiert die Schweregrade für Logmeldungen im Logging-System.
   Die Stufen beinhalten:
       - DEBUG: Für detaillierte Debug-Informationen während der Entwicklung.
       - INFO: Für allgemeine Systemoperationen und Informationsmeldungen.
       - WARNING: Für potenzielle Probleme, die Aufmerksamkeit erfordern könnten.
       - CRITICAL: Für schwerwiegende Fehler, die die Systemstabilität gefährden.
   Zu jeder Stufe wird eine typische Einsatzbeschreibung angegeben.

2. FusionLogRecord (dataclass):
   Dient als strukturierter Datencontainer für Logeinträge.
   Er fasst alle relevanten Metadaten eines Logeintrags zusammen und sorgt so für
   ein threadsicheres Format. Zu den Attributen gehören:
       - logger (fusion_logger): Die erzeugende Logger-Instanz.
       - level (FusionLogLevel): Schweregrad des Log-Ereignisses.
       - message (str): Die rohe Lognachricht.
       - timestamp (float): Unix-Zeitstempel, wann der Logeintrag erstellt wurde.
       - hostname (str): Name des Systems, auf dem der Logeintrag generiert wurde.
       - process_id (int): Prozess-ID des erzeugenden Prozesses.
       - thread_id (int): Thread-ID des erzeugenden Threads.
       - exception (Exception): Bei Bedarf übergebene Exception.

Dependencies:
    - Standardbibliotheken: 'dataclasses', 'datetime', 'enum' und 'typing'
    - fusion_logger aus dem lokalen 'core'-Modul, welches in das Gesamtsystem integriert ist.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .core import FusionLogger  # Nur für Typüberprüfungen


class FusionLogLevel(Enum):
    """
    Enumeration, die die Schweregrade für Logmeldungen definiert.

    Attributes:
        DEBUG: Niedrigste Stufe für Entwicklerdiagnosen
        INFO: Allgemeine Systeminformationen
        WARNING: Potenzielle Problemstellen
        CRITICAL: Kritische Systemfehler
    """

    DEBUG = 0
    """
    Detaillierte Debug-Informationen, etwa:
        - Variablenzustände
        - Ablaufverfolgung
        - Temporäre Diagnoseausgaben
    """

    INFO = 1
    """
    Regelt allgemeine Systemoperationen, wie:
        - Erfolgreiche Transaktionen
        - Systemstart und -shutdown
        - Konfigurationsänderungen
    """

    WARNING = 2
    """
    Warnt vor möglichen, aber behandelbaren Problemen, etwa:
        - Unerwartete Zustände
        - Deprecation-Hinweise
        - Engpässe bei Ressourcen
    """

    CRITICAL = 3
    """
    Signalisiert schwerwiegende Fehler, bei denen:
        - Nicht behandelbare Ausnahmen
        - Datenverluste
        - Kritische Abhängigkeitsfehler
      auftreten können.
    """


@dataclass
class FusionLogRecord:
    """
    Datencontainer für strukturierte Logginginformationen.

    Kapselt alle relevanten Metadaten eines Logeintrags in einem threadsicheren Format.

    Attributes:
        logger (FusionLogger): Referenz auf die erzeugende Logger-Instanz.
        level (FusionLogLevel): Schweregrad des Log-Ereignisses.
        message (str): Die Rohlognachricht.
        timestamp (float): Unix-Zeitstempel der Erstellung.
        hostname (str): Name des Systems, auf dem der Logeintrag erstellt wurde.
        process_id (int): Prozess-ID des Erzeugers.
        thread_id (int): Thread-ID des Erzeugers.
        exception (Exception): Optional übergebene Exception.
    """

    logger: "FusionLogger"
    """
    Referenz auf den Logger, der den Eintrag erzeugt hat.
    """

    level: FusionLogLevel
    """
    Schweregrad des Log-Ereignisses, z.B. DEBUG, INFO, WARNING oder CRITICAL.
    """

    message: str
    """
    Die ursprüngliche, unformatierte Nachricht des Logeintrags.
    """

    timestamp: float
    """
    Erstellungszeitpunkt des Logeintrags als Unix-Zeitstempel (UTC).
    """

    hostname: str
    """
    Name des Systems, auf dem der Logeintrag generiert wurde.
    """

    process_id: int
    """
    Prozess-ID desjenigen Prozesses, der den Eintrag erzeugt hat.
    """

    thread_id: int
    """
    Thread-ID desjenigen Threads, der den Eintrag erzeugt hat.
    """

    exception: Exception
    """
    Eventuell mitgelieferte Exception, die beim Logging aufgetreten ist.
    """

    files: set[str]
    """
    Dateien, in die die Nachrichten geschrieben werden.
    """


class Token:
    """
    Abstrakte Basisklasse für Token, die in der Logformatierung verwendet werden.
    """

    def apply(self, record: FusionLogRecord, built: str):
        """
        Wendet das Token auf den übergebenen Logeintrag an und baut den formatierten String auf.

        Args:
            record (FusionLogRecord): Der Logeintrag, der formatiert werden soll.
            built (str): Der bisher formatierte String.

        Returns:
            str: Der aktualisierte String nach Anwendung des Tokens.
        """
        pass  # Diese Methode dient als Platzhalter und sollte in abgeleiteten Klassen implementiert werden.


class LiteralToken(Token):
    """
    Token, das einen Literalstring ohne weitere Formatierung direkt anhängt.
    """

    def __init__(self, literal: str):
        """
        Initialisiert einen LiteralToken mit dem übergebenen Literalstring.

        Args:
            literal (str): Der Literalstring, der angehängt wird.
        """
        self.literal = literal

    def apply(self, record: FusionLogRecord, built: str) -> str:
        """
        Hängt den Literalstring an den bereits gebauten String an.

        Args:
            record (FusionLogRecord): Der Logeintrag (wird hier nicht verwendet).
            built (str): Der bisher formatierte String.

        Returns:
            str: Der String, erweitert um den Literalstring.
        """
        built += self.literal
        return built


class FormatToken(Token):
    """
    Token, das Platzhalter formatiert, indem es relevante Attribute aus einem Logeintrag extrahiert.
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
        Initialisiert einen FormatToken mit dem angegebenen Schlüssel.

        Args:
            key (str): Der Schlüssel, der angibt, welches Attribut aus dem Logeintrag formatiert werden soll.
        """
        self.key = key

    def apply(self, record: FusionLogRecord, built: str) -> str:
        """
        Wendet das FormatToken an, indem es den entsprechenden Attributswert aus dem Logeintrag
        an den bisherigen String anhängt.

        Args:
            record (FusionLogRecord): Der Logeintrag mit allen relevanten Metadaten.
            built (str): Der bisher formatierte String.

        Returns:
            str: Der aktualisierte String nach Anwendung des FormatTokens.
        """
        # Überprüfe den Schlüssel und hänge den entsprechenden Wert an.
        if self.key == self._logger_name_format:
            built += record.logger.name  # Name des Loggers

        elif self.key == self._logger_scope_format:
            built += record.logger.scope  # Scope des Loggers

        elif self.key == self._timestamp_format:
            # Formatiere den Unix-Zeitstempel in ein lesbares Datum/Zeit-Format
            built += datetime.fromtimestamp(record.timestamp).strftime("%Y-%m-%d %H:%M:%S")

        elif self.key == self._level_format:
            built += record.level.name[:4]  # Verwende die ersten 4 Buchstaben des Schweregrads

        elif self.key == self._hostname_format:
            built += record.hostname  # Rechnername des Systems

        elif self.key == self._message_format:
            built += record.message  # Lognachricht

        elif self.key == self._process_id_format:
            built += str(record.process_id)  # Prozess-ID (in String umgewandelt, falls nötig)

        elif self.key == self._thread_id_format:
            built += str(record.thread_id)  # Thread-ID (in String umgewandelt, falls nötig)


        else:
            built += "UNKNOWN_FORMAT"  # Unbekannter Format-Key, Standardausgabe

        return built
