import queue
from queue import Queue
import threading

from FusionLogRecord import FusionLogRecord


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
        queue (Queue): Threadsichere Nachrichtenwarteschlange
        thread (ProcessingThread): Verarbeitungsthread für LogRecords
    """


    def __init__(self) -> None:
        """
        Initialisiert Warteschlange und startet Verarbeitungsthread.
        """
        self.queue = Queue()
        self.thread = self.ProcessingThread(self.queue)
        self.thread.start()


    def kill_thread(self) -> None:
        """
        Stoppt den Verarbeitungsthread sicher.
        """
        self.thread.stop()


    class ProcessingThread(threading.Thread):
        """
        Interner Thread für asynchrone Logverarbeitung.

        Attributes:
            queue (Queue): Referenz zur übergeordneten Verarbeitungswarteschlange
            stop_event (threading.Event): Steuerungsobjekt für Thread-Lebenszyklus
            _lock (threading.Lock): Sperre für threadsichere Queue-Zugriffe
        """
        _lock = threading.Lock()


        def __init__(self, record_queue: Queue) -> None:
            """
            Initialisiert Thread mit gegebener Warteschlange.

            Args:
                record_queue (Queue): Queue für eingehende LogRecords
            """
            super().__init__(daemon=True)
            self.queue = record_queue
            self.stop_event = threading.Event()


        def run(self):
            """
            Hauptschleife für kontinuierliche Verarbeitung von LogRecords.
            """
            while not self.stop_event.is_set():
                with self._lock:
                    record: FusionLogRecord = self.queue.get()
                    out: str = self.process_record(record)
                    print(out)


        def process_record(self, record) -> str:
            """
            Verarbeitet einzelne LogRecords (muss überschrieben werden).

            Args:
                record (FusionLogRecord): Zu verarbeitender Log-Eintrag

            Returns:
                str: Formatierte Ausgabezeichenkette

            Raises:
                NotImplementedError: Wenn nicht überschrieben
            """
            raise NotImplementedError("process_record muss in Subklassen implementiert werden")


        def stop(self):
            """Signalisiert dem Thread, sich sicher zu beenden."""
            self.stop_event.set()
