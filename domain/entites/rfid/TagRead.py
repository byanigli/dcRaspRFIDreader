from typing import Optional


class TagRead:
    def __init__(self, epc: str, rssi: Optional[int] = None, tid: Optional[str] = None):
        self.epc = epc
        self.rssi = rssi
        self.tid = tid

    def __repr__(self):
        return f"TagRead(epc={self.epc}, rssi={self.rssi}, tid={self.tid})"
