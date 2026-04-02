from abc import ABC, abstractmethod


class ITransport(ABC):
    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def disconnect(self) -> None:
        pass

    @abstractmethod
    def send(self, data: bytes) -> None:
        pass

    @abstractmethod
    def receive(self, size: int = 1024) -> bytes:
        pass

    @abstractmethod
    def is_connected(self) -> bool:
        pass