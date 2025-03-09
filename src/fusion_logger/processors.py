import threading
from queue import Queue

from .defs import FusionLogRecord


class FusionLogFormatter(object):
    def __init__(self, template: str):
        self.tokens: list = FusionLogFormatter.parse_template(template)

    @staticmethod
    def parse_template(template: str) -> list:
        tokens: list = list()
        position: int = 0
        while position < len(template):
            start: int = template.find("{", position)
            if (start == -1):



class SingletonMeta(type):
    """
    Metaklasse zur Implementierung eines threadsicheren Singleton Patterns.

    Attributes:
        _instances (dict): Speichert Singleton-Instanzen der erzeugten Klassen
        _lock (threading.Lock): Sperre für threadsichere Instanzerstellung
    """

    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        """
        Erstellt oder gibt vorhandene Klasseninstanz zurück.
        Threadsichere Implementierung durch Verwendung einer Lock.

        Args:
            *args: Variable Positionsargumente
            **kwargs: Variable Schlüsselwortargumente

        Returns:
            object: Einzige Instanz der Klasse
        """
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class FusionLogProcessor(metaclass=SingletonMeta):
    """
    Zentraler Prozessor für LogRecords mit Singleton-Implementierung.
    Verwaltet eine Verarbeitungswarteschlange und einen Hintergrundthread.

    Attributes:
        _queue (Queue): Threadsichere Nachrichtenwarteschlange
    """

    def __init__(self) -> None:
        self._queue = Queue()

    def process_record(self, record: FusionLogRecord) -> None:
        """
        Verarbeitet einzelne LogRecords (muss überschrieben werden).

        Args:
            record (FusionLogRecord): Zu verarbeitender Log-Eintrag

        Returns:
            str: Formatierte Ausgabezeichenkette

        Raises:
            NotImplementedError: Wenn nicht überschrieben
        """
        out: str = record.logger.formatter.apply(record)
        print(out)
