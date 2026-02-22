"""
Thread-safe Singleton Pattern Implementations in Python
"""

import threading


# =========================
# Singleton via __new__
# =========================
class DatabaseConnection:
    """
    Thread-safe Singleton class for database connection.
    Ensures only one instance exists.
    """

    _instance = None
    _lock = threading.Lock()
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not self.__class__._initialized:
            self.connection_string = "localhost:5432"
            self.connected = True
            self.__class__._initialized = True

    def execute_query(self, query: str) -> str:
        return f"Executing query: {query}"

    def get_connection_info(self) -> str:
        return f"Connected to: {self.connection_string}, Status: {self.connected}"


# =========================
# Singleton via Decorator
# =========================
def singleton(cls):
    """
    Thread-safe Singleton decorator.
    """
    instances = {}
    lock = threading.Lock()

    def get_instance(*args, **kwargs):
        if cls not in instances:
            with lock:
                if cls not in instances:
                    instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton
class Logger:
    """
    Singleton Logger using decorator pattern.
    """

    def __init__(self):
        self.logs = []

    def log(self, message: str) -> None:
        self.logs.append(message)

    def get_logs(self) -> list:
        return self.logs


# =========================
# Demonstration
# =========================
if __name__ == "__main__":
    # DatabaseConnection test
    db1 = DatabaseConnection()
    db2 = DatabaseConnection()

    print(db1.get_connection_info())
    print(f"db1 is db2: {db1 is db2}")

    # Logger test
    logger1 = Logger()
    logger2 = Logger()

    logger1.log("First message")
    logger2.log("Second message")

    print(f"logger1 is logger2: {logger1 is logger2}")
    print(logger1.get_logs())
