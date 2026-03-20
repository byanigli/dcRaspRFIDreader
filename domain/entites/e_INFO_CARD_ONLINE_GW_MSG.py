from dataclasses import dataclass


@dataclass
class e_INFO_CARD_ONLINE_GW_MSG:
    cmd = 0x00
    status: int  # 0 offline, 1 online
    rssi: int  # 0-255
    operator_name: str  # dynamic
    ip: bytes  # 4 byte
    netmask: bytes  # 4 byte
    gateway: bytes  # 4 byte
    dns1: bytes  # 4 byte
    version: bytes  # 4 byte
