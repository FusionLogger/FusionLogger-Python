from dataclasses import dataclass

from FusionLogLevel import FusionLogLevel
from FusionLogger import FusionLogger


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
