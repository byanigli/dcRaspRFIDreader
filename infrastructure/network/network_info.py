import os
import re
import socket
import netifaces
import subprocess

from domain.value_objects.Mqtt.Media import Media


class NetworkInfo:

    @staticmethod
    def _get_active_interface() -> str:
        return netifaces.gateways()["default"][netifaces.AF_INET][1]

    @staticmethod
    def get_local_ip_bytes() -> bytes:
        iface = NetworkInfo._get_active_interface()
        addr = netifaces.ifaddresses(iface)[netifaces.AF_INET][0]["addr"]
        return socket.inet_aton(addr)

    @staticmethod
    def get_netmask_bytes() -> bytes:
        iface = NetworkInfo._get_active_interface()
        netmask = netifaces.ifaddresses(iface)[netifaces.AF_INET][0]["netmask"]
        return socket.inet_aton(netmask)

    @staticmethod
    def get_gateway_bytes() -> bytes:
        gateway = netifaces.gateways()["default"][netifaces.AF_INET][0]
        return socket.inet_aton(gateway)

    @staticmethod
    def get_dns1_bytes() -> bytes:
        try:
            with open("/etc/resolv.conf", "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("nameserver"):
                        dns = line.split()[1]
                        return socket.inet_aton(dns)
        except Exception:
            pass

        return socket.inet_aton("8.8.8.8")

    @staticmethod
    def get_media_type() -> Media:
        iface = NetworkInfo._get_active_interface().lower()
        ssid = NetworkInfo.get_wifi_ssid()

        print("iface:", iface)
        print("ssid:", ssid)

        # Linux wireless
        if os.path.exists(f"/sys/class/net/{iface}/wireless"):
            return Media.WIFI

        # SSID varsa WiFi kabul et
        if ssid:
            return Media.WIFI

        # Linux interface tahmini
        if iface.startswith("wl"):
            return Media.WIFI

        return Media.ETH

    @staticmethod
    def get_wifi_ssid() -> str:
        iface = NetworkInfo._get_active_interface()

        # Linux
        try:
            result = subprocess.check_output(
                ["iwgetid", "-r"],
                stderr=subprocess.DEVNULL
            ).decode().strip()
            if result:
                return result
        except Exception:
            pass

        # macOS - en sağlam yöntem
        try:
            result = subprocess.check_output(
                ["networksetup", "-getairportnetwork", iface],
                stderr=subprocess.DEVNULL
            ).decode().strip()

            # örnek: "Current Wi-Fi Network: MyWifi"
            if "Current Wi-Fi Network:" in result:
                return result.split("Current Wi-Fi Network:", 1)[1].strip()
        except Exception:
            pass

        # macOS alternatif
        try:
            airport_path = (
                "/System/Library/PrivateFrameworks/Apple80211.framework"
                "/Versions/Current/Resources/airport"
            )
            result = subprocess.check_output(
                [airport_path, "-I"],
                stderr=subprocess.DEVNULL
            ).decode()

            match = re.search(r"^\s*SSID:\s*(.+)$", result, re.MULTILINE)
            if match:
                return match.group(1).strip()
        except Exception:
            pass

        return ""

    @staticmethod
    def get_wifi_rssi() -> int:
        if NetworkInfo.get_media_type() != Media.WIFI:
            return 0

        iface = NetworkInfo._get_active_interface()

        # Linux
        try:
            output = subprocess.check_output(
                ["iwconfig", iface],
                stderr=subprocess.DEVNULL
            ).decode()

            match = re.search(r"Signal level=(-?\d+)\s*dBm", output)
            if match:
                rssi_dbm = int(match.group(1))
                quality = 2 * (rssi_dbm + 100)
                return max(0, min(100, quality))
        except Exception:
            pass

        # macOS
        try:
            airport_path = (
                "/System/Library/PrivateFrameworks/Apple80211.framework"
                "/Versions/Current/Resources/airport"
            )
            output = subprocess.check_output(
                [airport_path, "-I"],
                stderr=subprocess.DEVNULL
            ).decode()

            match = re.search(r"agrCtlRSSI:\s*(-?\d+)", output)
            if match:
                rssi_dbm = int(match.group(1))
                quality = 2 * (rssi_dbm + 100)
                return max(0, min(100, quality))
        except Exception:
            pass

        return 0