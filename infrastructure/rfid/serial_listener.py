import threading
import time
from domain.interfaces.rfid.IRfidReader import IRfidReader
from domain.services.mqtt_messages import MqttMessages


class SerialRFIDListener(threading.Thread):
    def __init__(self, reader, publisher):
        super().__init__(daemon=True)
        self.reader: IRfidReader = reader
        self.publisher = publisher
        self.running = True
        self.last_seen = {}
        self.dedup_seconds = 60  # 1 dakika
        self.cleanup_interval = 300  # 5 dk
        self.last_cleanup = time.time()
        self.mqtt_messages = MqttMessages()

    def _can_process_epc(self, epc: str, now: float) -> bool:
        last_time = self.last_seen.get(epc)
        if last_time is None:
            self.last_seen[epc] = now
            return True

        if (now - last_time) > self.dedup_seconds:
            self.last_seen[epc] = now
            return True

        return False

    def _cleanup_old_epcs(self, now: float):
        if now - self.last_cleanup < self.cleanup_interval:
            return

        expire_before = now - self.dedup_seconds
        self.last_seen = {
            epc: ts for epc, ts in self.last_seen.items()
            if ts > expire_before
        }
        self.last_cleanup = now

    def run(self):
        try:
            self.reader.connect()
            print("RFID listener başladı")
            print(self.reader.__class__.__name__)

            while self.running:
                try:
                    tags = self.reader.inventory()
                    now = time.time()

                    self._cleanup_old_epcs(now)

                    for tag in tags:
                        if not self._can_process_epc(tag.epc, now):
                            continue

                        if self.reader.__class__.__name__ == "RruReader":
                            antenna = self.reader.getConfig().antennaNumber
                            packet, topic = self.mqtt_messages.get_UHF_Read_Tag_Message(
                                antenna, tag.epc, 255
                            )

                            print(
                                f"[RFID READ] "
                                f"reader={self.reader.__class__.__name__} "
                                f"antenna={antenna} "
                                f"epc={tag.epc} "
                                f"time={time.strftime('%H:%M:%S')} "
                                f"topic={topic}"
                            )

                            self.publisher.publish(topic, packet)

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
