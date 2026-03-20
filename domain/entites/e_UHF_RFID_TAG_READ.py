from dataclasses import dataclass


@dataclass
class e_UHF_RFID_TAG_READ:
    cmd: 0x04
    antennaNumber: int
    tidLength: int
    tid: bytes
    epcLength: int
    epc: bytes
    rssi: int
    lastSeen: bytes
