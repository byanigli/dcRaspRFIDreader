from dataclasses import dataclass
from typing import Optional


@dataclass
class e_UHF_RFID_TAG_READ:
    cmd: int = 0x04
    antennaNumber: int = 0
    tidLength: int = 0
    tid: Optional[bytes] = None
    epcLength: int = 0
    epc: bytes = b''
    rssi: int = 0
    lastSeen: bytes = b''