import json
import threading
import time

from domain.entites.ProtocolFrame import ProtocolFrame
from domain.entites.e_UHF_RFID_TAG_READ import e_UHF_RFID_TAG_READ
from domain.interfaces.rfid.IRfidReader import IRfidReader
from domain.services.mqtt_frame_builder import FrameBuilder
from domain.services.mqtt_messages import MqttMessages
from domain.services.uhfRfidTagReadBuilder import uhfRfidTagReadBuilder

class SerialRFIDListener(threading.Thread):
    def __init__(self, reader, publisher):
        super().__init__(daemon=True)
        self.reader:IRfidReader  = reader
        self.publisher = publisher
        self.running = True
        self.last_seen = {}
        self.dedup_seconds = 2
        self.mqtt_messages = MqttMessages()

    def run(self):
        try:
            self.reader.connect()
            print("RFID listener başladı")
            print(self.reader.__class__.__name__)

            while self.running:
                try:
                    tags = self.reader.inventory()
                    now = time.time()

                    for tag in tags:
                        if tag.epc not in self.last_seen or (now - self.last_seen[tag.epc]) > self.dedup_seconds:

                            if self.reader.__class__.__name__ == "RruReader":
                                self.last_seen[tag.epc] = now
                                payload = self.mqtt_messages.get_UHF_Read_Tag_Message(self.reader.getConfig().antennaNumber, tag.epc, 255)
                                self.publisher.publish(payload[1],payload[0])

                    time.sleep(0.1)

                except Exception as e:
                    print("Listener hata:", e)
                    time.sleep(1)

        finally:
            try:
                self.reader.disconnect()
            except Exception:
                pass
            print("RFID listener durdu")
