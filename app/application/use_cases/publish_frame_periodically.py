import time
from typing import Callable

from infrastructure.Mqtt.MqttPublisher import MqttPublisher


class PublishFramePeriodically:
    def __init__(
        self,
        publisher: MqttPublisher,
        frame_factory: Callable[[], bytes],
        interval_seconds: float,
    ):
        self._publisher = publisher
        self._frame_factory = frame_factory
        self._interval_seconds = interval_seconds

    def run(self) -> None:
        self._publisher.connect()

        try:
            while True:
                packet = self._frame_factory()
                self._publisher.publish(packet)
                print("Published:", " ".join(f"0x{b:02X}" for b in packet))
                time.sleep(self._interval_seconds)
        finally:
            self._publisher.disconnect()