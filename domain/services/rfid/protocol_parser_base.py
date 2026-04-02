class ProtocolParserBase:
    @staticmethod
    def verify_crc(frame: bytes) -> bool:
        if len(frame) < 5:
            return False

        payload = frame[:-2]
        recv_crc_l = frame[-2]
        recv_crc_h = frame[-1]
        recv_crc = recv_crc_l | (recv_crc_h << 8)

        from domain.services.rfid.rru_protocol import RruProtocol
        calc_crc = RruProtocol.crc16(payload)

        return recv_crc == calc_crc