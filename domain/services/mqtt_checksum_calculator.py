from domain.value_objects.Mqtt.Media import Media
from domain.value_objects.Mqtt.MqttMessageType import MqttMessageType


class MQTTChecksumCalculator:
    INITIAL_VALUE = 1

    @classmethod
    def calculate(
        cls,
        nw_version: int,
        source_address: bytes,
        repeater_address: bytes,
        destination_address: bytes,
        next_hop: int,
        media: Media,
        msg_no: int,
        msg_type: MqttMessageType,
        data: bytes,
    ) -> int:

        buffer = bytearray()

        buffer.append(nw_version & 0xFF)
        buffer.extend(source_address)
        buffer.extend(repeater_address)
        buffer.extend(destination_address)
        buffer.append(next_hop & 0xFF)
        buffer.append(media.value)
        buffer.append(msg_no & 0xFF)
        buffer.append(msg_type.value)
        buffer.extend(data)

        return (cls.INITIAL_VALUE + sum(buffer)) % 256