from abc import ABC, abstractmethod
from typing import List

from domain.entites.rfid.ReaderConfig import ReaderConfig
from domain.entites.rfid.TagRead import TagRead


class IRfidReader(ABC):
    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def disconnect(self) -> None:
        pass

    @abstractmethod
    def get_reader_info(self) -> bytes:
        pass

    @abstractmethod
    def get_reader_work_mode(self) -> bytes:
        pass

    @abstractmethod
    def inventory(self) -> List[TagRead]:
        pass

    def getConfig(self)-> ReaderConfig:
        pass

