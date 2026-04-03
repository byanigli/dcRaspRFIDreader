import time

from domain.entites.rfid.ReaderConfig import ReaderConfig
from domain.services.mqtt_messages import MqttMessages
from infrastructure.Mqtt.MqttPublisher import MqttPublisher
from infrastructure.rfid.rru_reader import RruReader
from infrastructure.rfid.serial_listener import SerialRFIDListener
from infrastructure.rfid.serial_transport import SerialTransport


def create_reader_and_listener(port: str, publisher: MqttPublisher):
    config = ReaderConfig(
        port=port,
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

    print(f"{port} bağlanıyor...")
    reader.connect()

    raw = reader.get_reader_info()
    print(f"{port} RAW READER INFO:", raw.hex().upper())
    print(f"{port} PARSED READER INFO:", reader.get_reader_info_parsed_from_raw(raw))
    print("---------------------------------------------------------------------------------")
    raw = reader.set_reader_power(28)
    print(f"{port} RAW SET READER:", raw.hex().upper())

    tags = reader.inventory()
    print(f"{port} INVENTORY TAGS:", tags)

    reader.disconnect()

    print(f"{port} listener başlatılıyor...")

    transport2 = SerialTransport(
        port=config.port,
        baudrate=config.baudrate,
        timeout=config.timeout
    )

    reader2 = RruReader(transport2, config)
    listener = SerialRFIDListener(reader2, publisher)
    listener.start()

    return listener


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

    listeners = []

    try:
        publisher.connect()

        packet, topic = mqtt_messages.get_online_message(True)
        publisher.publish(topic, packet)

        print("Online mesaj gönderildi.")

        ports = ["/dev/ttyUSB0", "/dev/ttyUSB1"]

        #ports = ["/dev/tty.usbserial-0001"]

        for port in ports:
            try:
                listener = create_reader_and_listener(port, publisher)
                listeners.append(listener)
            except Exception as e:
                print(f"{port} başlatılırken hata: {e}")

        if not listeners:
            print("Hiçbir reader başlatılamadı.")
            return

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("CTRL+C ile çıkılıyor...")

    except Exception as e:
        print(f"HATA: {e}")

    finally:
        for listener in listeners:
            try:
                listener.running = False
            except Exception:
                pass

        try:
            publisher.disconnect()
        except Exception:
            pass


if __name__ == "__main__":
    main()