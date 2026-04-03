class RruProtocol:
    PRESET_VALUE = 0xFFFF
    POLYNOMIAL = 0x8408

    CMD_GET_READER_INFO = 0x21
    CMD_INVENTORY = 0x01  # bunu cihaz dokümanındaki gerçek inventory code ile güncelle
    CMD_READ = 0x02  # bunu da gerçek read cmd ile güncelle
    CMD_SET_POWER = 0x2F

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
        payload = body + bytes([crc & 0xFF, (crc >> 8) & 0xFF])
        print(f"payload: {payload.hex()} \n")
        return payload

    @classmethod
    def get_reader_info(cls, address: int = 0x00) -> bytes:
        return cls.build_frame(address, cls.CMD_GET_READER_INFO)

    @classmethod
    def set_reader_uhfPower(cls, value: int, address: int = 0x00) -> bytes:
        if value < 0 or value > 30:
            raise ValueError("Value must be between 0 and 30")
        return cls.build_frame(address, cls.CMD_SET_POWER, bytes([value]))

    @classmethod
    def inventory(cls, address: int = 0x00, payload: bytes = b"") -> bytes:
        return cls.build_frame(address, cls.CMD_INVENTORY, payload)

    @classmethod
    def read_tid(cls, address: int = 0x00, payload: bytes = b"") -> bytes:
        return cls.build_frame(address, cls.CMD_READ, payload)
