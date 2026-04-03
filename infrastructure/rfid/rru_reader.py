from tkinter import BooleanVar
from typing import List

from domain.entites.rfid.ReaderConfig import ReaderConfig
from domain.entites.rfid.TagRead import TagRead
from domain.interfaces.rfid.IRfidReader import IRfidReader
from domain.interfaces.rfid.ITransport import ITransport
from domain.services.rfid.RruResponseParser import RruResponseParser
from domain.services.rfid.rru_protocol import RruProtocol


class RruReader(IRfidReader):
    def __init__(self, transport: ITransport, config: ReaderConfig):
        self.transport = transport
        self.config = config

    def connect(self) -> None:
        self.transport.connect()

    def disconnect(self) -> None:
        self.transport.disconnect()

    def get_reader_info(self) -> bytes:
        cmd = RruProtocol.get_reader_info(self.config.address)
        self.transport.send(cmd)
        return self.transport.receive(256)

    def get_reader_info_parsed(self) -> dict:
        raw = self.get_reader_info()
        return RruResponseParser.parse_reader_info(raw)

    def set_reader_power(self, power: int) -> bytes:
        raw = RruProtocol.set_reader_uhfPower(power)
        self.transport.send(raw)
        return self.transport.receive(256)

    def inventory(self) -> List[TagRead]:
        cmd = RruProtocol.inventory(self.config.address)
        self.transport.send(cmd)
        raw = self.transport.receive(1024)
        return RruResponseParser.parse_inventory(raw)

    def stop_inventory(self) -> bool:


    def get_reader_info_parsed_from_raw(self, raw: bytes) -> dict:
        return RruResponseParser.parse_reader_info(raw)
