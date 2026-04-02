import time

from domain.entites.rfid.ReaderConfig import ReaderConfig
from domain.services.mqtt_messages import MqttMessages
from infrastructure.Mqtt.MqttPublisher import MqttPublisher
from infrastructure.rfid.rru_reader import RruReader
from infrastructure.rfid.serial_listener import SerialRFIDListener
from infrastructure.rfid.serial_transport import SerialTransport


def main() -> None:
    mqtt_messages = MqttMessages()

    publisher = MqttPublisher(
        host="217.195.207.251",
        port=1883,
        lwtMessages=mqtt_messages.get_online_message(False),
        disconnectMessages=mqtt_messages.get_online_message(False),
        client_id="dc-rfid-raspberry",
        username="okan",
        password="Okan1234.",
    )

    config = ReaderConfig(
        port="/dev/ttyUSB0",
        baudrate=57600,
        timeout=1,
        address=0x00
    )

    transport = SerialTransport(
        port=config.port,
        baudrate=config.baudrate,
        timeout=config.timeout
    )

    reader = RruReader(transport, config)
    listener = None

    try:
        publisher.connect()

        packet, topic = mqtt_messages.get_online_message(True)
        publisher.publish(topic, packet)

        print("Online mesaj gönderildi.")

        # DEBUG
        reader.connect()

        raw = reader.get_reader_info()
        print("RAW READER INFO:", raw.hex().upper())
        print("PARSED READER INFO:", reader.get_reader_info_parsed_from_raw(raw))

        # inventory test
        tags = reader.inventory()
        print("INVENTORY TAGS:", tags)

        reader.disconnect()

        print("RFID listener başlatılıyor...")

        transport2 = SerialTransport(
            port=config.port,
            baudrate=config.baudrate,
            timeout=config.timeout
        )
        reader2 = RruReader(transport2, config)
        listener = SerialRFIDListener(reader2, publisher)
        listener.start()

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("CTRL+C ile çıkılıyor...")
        if listener:
            listener.running = False

    except Exception as e:
        print(f"HATA: {e}")
        if listener:
            listener.running = False

    finally:
        try:
            if listener:
                listener.running = False
        except Exception:
            pass

        try:
            reader.disconnect()
        except Exception:
            pass

        try:
            publisher.disconnect()
        except Exception:
            pass


if __name__ == "__main__":
    main()