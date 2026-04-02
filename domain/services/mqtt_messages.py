import time
import uuid
from typing import Optional

from domain.entites.ProtocolFrame import ProtocolFrame
from domain.entites.e_INFO_CARD_ONLINE_GW_MSG import e_INFO_CARD_ONLINE_GW_MSG
from domain.entites.e_UHF_RFID_TAG_READ import e_UHF_RFID_TAG_READ
from domain.services.card_status_builder import CardStatusBuilder
from domain.services.mqtt_frame_builder import FrameBuilder
from domain.services.uhfRfidTagReadBuilder import uhfRfidTagReadBuilder
from domain.value_objects.Mqtt.Media import Media
from domain.value_objects.Mqtt.MqttMessageType import MqttMessageType
from infrastructure.network.network_info import NetworkInfo


class MqttMessages:
    def __init__(self):
        self.source = uuid.getnode().to_bytes(8, "little")
        self.destination = bytes([0xFF] * 8)
        self.repeater = bytes([0x00] * 8)
        self.media = NetworkInfo.get_media_type()
        print(self.media)
        source_id = int.from_bytes(self.source, byteorder="little")
        self.topic_card_status = f"/device/status/{source_id}"
        self.topic_req = f"/device/messages/req/{source_id}"

    def get_online_message(self, is_online: bool) -> tuple[bytes, str]:
        message = e_INFO_CARD_ONLINE_GW_MSG(
            status=0x01 if is_online else 0x00,
            rssi=100 if self.media == Media.ETH else NetworkInfo.get_wifi_rssi(),
            operator_name="LAN-ETHERNET" if self.media == Media.ETH else NetworkInfo.get_wifi_ssid(),
            ip=NetworkInfo.get_local_ip_bytes(),
            netmask=NetworkInfo.get_netmask_bytes(),
            gateway=NetworkInfo.get_gateway_bytes(),
            dns1=NetworkInfo.get_dns1_bytes(),
            version=b"\x01\x00\x00\x00",
        )

        payload = CardStatusBuilder.build(message)

        frame = ProtocolFrame(
            version=1,
            source=self.source,
            repeater=self.repeater,
            destination=self.destination,
            next_hop=0,
            media=self.media,
            msg_no=0,
            ack=0,
            msg_type=MqttMessageType.e_INFOALARM_INFO,
            dataLen=len(payload),
            payload=payload,
        )

        packet = FrameBuilder().build(frame)
        return packet, self.topic_card_status

    def get_UHF_Read_Tag_Message(
            self,
            antennaNumber: int,
            epc: bytes,
            rssi: int,
            tid: Optional[bytes] = None
    ) -> tuple[bytes, str]:
        message = e_UHF_RFID_TAG_READ(
            antennaNumber=antennaNumber,
            tidLength=len(tid) if tid is not None else 0,
            tid=tid,
            epcLength=len(epc),
            epc=epc,
            rssi=rssi,
            lastSeen=int(time.time()).to_bytes(8, byteorder='little', signed=True)
        )

        payload = uhfRfidTagReadBuilder.build(message)
        frame = ProtocolFrame(
            version=1,
            source=self.source,
            repeater=self.repeater,
            destination=self.destination,
            next_hop=0,
            media=self.media,
            msg_no=0,
            ack=0,
            msg_type=MqttMessageType.e_INFOALARM_INFO,
            dataLen=len(payload),
            payload=payload,
        )

        packet = FrameBuilder().build(frame)
        return packet, self.topic_req
