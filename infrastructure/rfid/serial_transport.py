import serial
from domain.interfaces.rfid.ITransport import ITransport


class SerialTransport(ITransport):
    def __init__(self, port: str, baudrate: int = 57600, timeout: float = 1.0):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self._ser = None

    def connect(self) -> None:
        if self._ser and self._ser.is_open:
            return

        self._ser = serial.Serial(
            port=self.port,
            baudrate=self.baudrate,
            timeout=self.timeout
        )

    def disconnect(self) -> None:
        if self._ser and self._ser.is_open:
            self._ser.close()

    def send(self, data: bytes) -> None:
        if not self.is_connected():
            raise ConnectionError("Serial port bağlı değil")
        self._ser.write(data)

    def receive(self, size: int = 1024) -> bytes:
        if not self.is_connected():
            raise ConnectionError("Serial port bağlı değil")
        return self._ser.read(size)

    def is_connected(self) -> bool:
        return self._ser is not None and self._ser.is_open