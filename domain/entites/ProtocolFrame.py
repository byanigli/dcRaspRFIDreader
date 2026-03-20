from dataclasses import dataclass

from domain.value_objects.Mqtt import Media
from domain.value_objects.Mqtt.MqttMessageType import MqttMessageType


@dataclass
class ProtocolFrame:
    version: int
    source: bytes
    repeater: bytes
    destination: bytes
    next_hop: int
    media: Media
    msg_no: int
    ack: int
    msg_type: MqttMessageType
    dataLen:int
    payload: bytes