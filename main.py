import time

import serial

from domain.services.mqtt_messages import MqttMessages
from infrastructure.Mqtt.MqttPublisher import MqttPublisher
import socket


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

    PORT = 6000
    NETWORK = "192.168.1."
    TIMEOUT = 0.5

    for i in range(1, 256):
        ip = NETWORK + str(i)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(TIMEOUT)

        try:
            result = s.connect_ex((ip, PORT))
            if result == 0:
                print(f"[OPEN] {ip}:{PORT}")
        except Exception:
            pass
        finally:
            s.close()

    print("[CLOSE]")
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
