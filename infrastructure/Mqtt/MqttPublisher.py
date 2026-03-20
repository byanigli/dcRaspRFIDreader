import time
from typing import Optional
import uuid
import paho.mqtt.client as mqtt


class MqttPublisher:
    def __init__(
            self,
            host: str,
            port: int,
            lwtMessages: tuple[bytes, str],
            disconnectMessages: tuple[bytes, str],
            client_id: Optional[str] = None,
            username: Optional[str] = None,
            password: Optional[str] = None,
    ):
        self._host = host
        self._port = port
        self._client_id = client_id or f"dc-rfid-{uuid.uuid4()}"

        self._client = mqtt.Client(client_id=self._client_id)
        self._is_connected = False

        if username is not None:
            self._client.username_pw_set(username, password)

        self._client.on_connect = self._on_connect
        self._client.on_disconnect = self._on_disconnect

        # 🔥 reconnect
        self._client.reconnect_delay_set(min_delay=1, max_delay=10)
        self.lwt_messages = lwtMessages
        self.disconnectMessages = disconnectMessages

    def _on_connect(self, client, userdata, flags, rc, properties=None):
        self._is_connected = (rc == 0)
        print("MQTT connected:", rc)

    def _on_disconnect(self, client, userdata, rc, properties=None):
        self._is_connected = False
        print("MQTT disconnected:", rc)

    def connect(self) -> None:
        try:
            # 🔥 LWT (broker disconnect olursa otomatik gönderilir)
            if self.lwt_messages:
                self._client.will_set(
                    topic=self.lwt_messages[1],
                    payload=self.lwt_messages[0],
                    qos=1,
                    retain=False
                )

            self._client.connect(self._host, self._port, 60)

        except Exception as e:
            raise RuntimeError(f"MQTT connect error: {e}")

        self._client.loop_start()

        timeout = time.time() + 5
        while not self._is_connected:
            if time.time() > timeout:
                raise TimeoutError("MQTT broker'a bağlanılamadı")
            time.sleep(0.1)

    def publish(self, topic: str, payload: bytes) -> None:
        if not self._is_connected:
            raise RuntimeError("MQTT not connected")

        result = self._client.publish(topic, payload=payload, qos=1, retain=topic.startswith("/device/status/"))
        result.wait_for_publish()

        if result.rc != mqtt.MQTT_ERR_SUCCESS:
            raise RuntimeError(f"MQTT publish failed: {result.rc}")

    def disconnect(self) -> None:
        if self.disconnectMessages:
            self.publish(self.disconnectMessages[1], self.disconnectMessages[0])
        self._client.loop_stop()
        self._client.disconnect()
