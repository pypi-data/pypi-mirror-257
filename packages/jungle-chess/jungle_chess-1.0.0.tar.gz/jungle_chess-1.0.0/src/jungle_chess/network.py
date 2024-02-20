from abc import ABC, abstractmethod
from typing import Optional
import socket
import select
import threading

HOST = ""
PORT = 5555


class Host(ABC):
    """Abstract host."""

    def __init__(self) -> None:
        self._is_connected = False
        self._cancel = False
        self._mutex = threading.Lock()

    @property
    def is_connected(self) -> bool:
        return self._is_connected

    @abstractmethod
    def connect(self) -> None:
        """Connect."""
        pass

    @abstractmethod
    def disconnect(self, data) -> None:
        """Disconnect."""
        pass

    @abstractmethod
    def send(self, data) -> None:
        """Send."""
        pass

    @abstractmethod
    def recv(self) -> Optional[bytes]:
        """Recieve."""
        pass


class Server(Host):
    """Server."""

    def __init__(self) -> None:
        super().__init__()
        self._conn = None

        try:
            self._sock = socket.create_server((HOST, PORT), backlog=1)
        except socket.error as e:
            print(str(e))

    def connect(self) -> None:
        try:
            inputs = [self._sock]
            while not self._is_connected:
                if self._cancel:
                    self._mutex.acquire()
                    self._cansel = False
                    self._mutex.release()
                    return
                rlist, wlist, xlist = select.select(inputs, [], [], 1)
                for s in rlist:
                    if s is self._sock:
                        self._conn, addr = self._sock.accept()
                        self._conn.setblocking(False)

                        self._mutex.acquire()
                        self._is_connected = True
                        self._mutex.release()

            print(f"Connected by {addr}")
        except:
            pass

    def disconnect(self) -> None:
        self._mutex.acquire()
        self._cancel = True
        self._is_connected = False
        self._mutex.release()

        if self._conn is not None:
            self._conn.close()
        self._conn = None

    def send(self, data) -> None:
        self._conn.send(data)

    def recv(self) -> Optional[bytes]:
        try:
            return self._conn.recv(4096)
        except:
            return None


class Client(Host):
    """Client."""

    def __init__(self, host: str = HOST) -> None:
        super().__init__()
        self._address = (host, PORT)
        self._sock = None

    def connect(self) -> None:
        while not self.is_connected:
            if self._cancel:
                self._mutex.acquire()
                self._cansel = False
                self._mutex.release()
                return
            try:
                self._sock = socket.create_connection(self._address)
                self._mutex.acquire()
                self._is_connected = True
                self._mutex.release()
            except:
                pass
        self._sock.setblocking(False)
        print(f"Connected to {self._address}")

    def disconnect(self) -> None:
        self._mutex.acquire()
        self._cancel = True
        self._is_connected = False
        self._mutex.release()
        if self._sock is not None:
            self._sock.close()

    def send(self, data) -> None:
        self._sock.send(data)

    def recv(self) -> Optional[bytes]:
        try:
            return self._sock.recv(4096)
        except:
            return None
