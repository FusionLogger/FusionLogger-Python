from enum import Enum


class FusionLogLevel(Enum):
    """
    Definiert die Schweregrade für Logmeldungen in einem mehrstufigen Logging-System.

    Attributes:
        Debug: Niedrigste Stufe für Entwicklerdiagnosen
        Info: Allgemeine Systeminformationen
        Warning: Potenzielle Probleme
        Critical: Kritische Systemfehler
    """

    Debug = 0,
    """
    Verwendet für detaillierte Debug-Informationen während der Entwicklung.

    Typische Anwendungen:
        - Variablenzustände
        - Ablaufverfolgung
        - Temporäre Diagnoseausgaben
    """

    Info = 1,
    """
    Beschreibt reguläre Systemoperationen.

    Wichtige Ereignisse:
        - Erfolgreiche Transaktionen
        - Systemstart/Shutdown
        - Konfigurationsänderungen
    """

    Warning = 2,
    """
    Kennzeichnet potenzielle Problemstellen.

    Anwendungsfälle:
        - Unerwartete aber behandelbare Zustände
        - Deprecation-Hinweise
        - Ressourcenengpässe
    """

    Critical = 3
    """
    Dokumentiert schwerwiegende Systemfehler.

    Wird verwendet bei:
        - Nicht behandelbaren Ausnahmen
        - Datenverlusten
        - Kritischen Abhängigkeitsfehlern
    """
