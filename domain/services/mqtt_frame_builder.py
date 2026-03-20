from domain.entites.ProtocolFrame import ProtocolFrame
from domain.services.mqtt_checksum_calculator import MQTTChecksumCalculator


class FrameBuilder:
    def build(self, frame: ProtocolFrame) -> bytes:
        self._validate(frame)

        body = bytearray()
        body.append(frame.version & 0xFF)
        body.extend(frame.source)
        body.extend(frame.repeater)
        body.extend(frame.destination)
        body.append(frame.next_hop & 0xFF)
        body.append(frame.media.value)
        body.append(frame.msg_no & 0xFF)
        body.append(frame.ack & 0xFF)
        body.append(frame.msg_type.value)
        body.append(frame.dataLen & 0xFF)
        body.extend(frame.payload)

        checksum = MQTTChecksumCalculator.calculate(
            nw_version=frame.version,
            source_address=frame.source,
            repeater_address=frame.repeater,
            destination_address=frame.destination,
            next_hop=frame.next_hop,
            media=frame.media,
            msg_no=frame.msg_no,
            msg_type=frame.msg_type,
            data=frame.payload,
        )

        body.append(checksum)
        return bytes(body)

    def _validate(self, frame: ProtocolFrame) -> None:
        if len(frame.source) != 8:
            raise ValueError("source_address must be 8 bytes")
        if len(frame.repeater) != 8:
            raise ValueError("repeater_address must be 8 bytes")
        if len(frame.destination) != 8:
            raise ValueError("destination_address must be 8 bytes")
