from typing import List

from domain.entites.rfid.TagRead import TagRead
from domain.services.rfid.protocol_parser_base import ProtocolParserBase


class RruResponseParser(ProtocolParserBase):
    @staticmethod
    def parse_reader_info(frame: bytes) -> dict:
        if not RruResponseParser.verify_crc(frame):
            raise ValueError("CRC hatalı")

        if len(frame) < 5:
            raise ValueError("Eksik frame")

        length = frame[0]
        addr = frame[1]
        cmd = frame[2]
        status = frame[3]
        data = frame[4:-2]
        print("data hep benden geliyor\n")
        return {
            "length": length,
            "address": addr,
            "cmd": cmd,
            "status": status,
            "data": data.hex().upper()
        }

    @staticmethod
    def parse_inventory(frame: bytes) -> List[TagRead]:
        if not RruResponseParser.verify_crc(frame):
            raise ValueError("CRC hatalı")

        # Burayı cihazın inventory response yapısına göre dolduracağız.
        # Şimdilik ham debug dönelim.
        length = frame[0]
        addr = frame[1]
        cmd = frame[2]
        status = frame[3]
        data = frame[4:-2]
        # TODO: status 2 & 4 multiple epc gönderme daha sonra yap:
        if cmd == 0x01 and status == 0x01:
            tags = []
            tag_count = data[0]
            print("tag",tag_count)
            index = 1
            for _ in range(tag_count):
                epc_len = data[index]
                index += 1
                epc = data[index:index + epc_len]
                index += epc_len
                tags.append(TagRead(epc))

            return tags

        return []
