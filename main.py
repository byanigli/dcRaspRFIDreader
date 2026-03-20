import time

import serial

from domain.services.mqtt_messages import MqttMessages
from infrastructure.Mqtt.MqttPublisher import MqttPublisher


def main() -> None:
    mqtt_messages = MqttMessages()
    publisher = MqttPublisher(
        host="217.195.207.251",
        port=1883,
        lwtMessages=mqtt_messages.get_online_message(False),
        disconnectMessages= mqtt_messages.get_online_message(False),
        client_id="dc-rfid-raspberry",
        username="okan",
        password="Okan1234.",
    )



    try:
        publisher.connect()

        mqtt_messages = MqttMessages()
        packet, topic = mqtt_messages.get_online_message(True)
        publisher.publish(topic, packet)

        print("Online mesaj gönderildi. Bekleniyor...")

        while True:
            time.sleep(1)  # sadece bekliyor

    except KeyboardInterrupt:
        print("CTRL+C ile çıkılıyor...")

    finally:
        try:
            publisher.disconnect()
        except Exception:
            pass


# use_case = PublishFramePeriodically(
#     publisher=publisher,
#     frame_factory=build_test_frame,
#     interval_seconds=5.0,
# )

# use_case.run()


if __name__ == "__main__":
    main()
