class RruProtocol:
    PRESET_VALUE = 0xFFFF
    POLYNOMIAL = 0x8408

    CMD_GET_READER_INFO = 0x21
    CMD_INVENTORY = 0x01   # bunu cihaz dokümanındaki gerçek inventory code ile güncelle
    CMD_READ = 0x02        # bunu da gerçek read cmd ile güncelle

    @classmethod
    def crc16(cls, data: bytes) -> int:
        crc = cls.PRESET_VALUE

        for b in data:
            crc ^= b
            for _ in range(8):
                if crc & 0x0001:
                    crc = (crc >> 1) ^ cls.POLYNOMIAL
                else:
                    crc >>= 1

        return crc & 0xFFFF

    @classmethod
    def build_frame(cls, address: int, cmd: int, payload: bytes = b"") -> bytes:
        # Len = Adr + Cmd + Data + CRC(2)
        length = 1 + 1 + len(payload) + 2
        body = bytes([length, address, cmd]) + payload
        crc = cls.crc16(body)
        return body + bytes([crc & 0xFF, (crc >> 8) & 0xFF])

    @classmethod
    def get_reader_info(cls, address: int = 0x00) -> bytes:
        return cls.build_frame(address, cls.CMD_GET_READER_INFO)

    @classmethod
    def inventory(cls, address: int = 0x00, payload: bytes = b"") -> bytes:
        return cls.build_frame(address, cls.CMD_INVENTORY, payload)

    @classmethod
    def read_tid(cls, address: int = 0x00, payload: bytes = b"") -> bytes:
        return cls.build_frame(address, cls.CMD_READ, payload)