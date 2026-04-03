from dataclasses import dataclass


@dataclass
class ReaderConfig:
    port: str
    baudrate: int = 57600
    timeout: float = 1.0
    address: int = 0x00
    antennaNumber: int = 0