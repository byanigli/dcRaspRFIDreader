from domain.entites.e_INFO_CARD_ONLINE_GW_MSG import e_INFO_CARD_ONLINE_GW_MSG


class CardStatusBuilder:

    @staticmethod
    def build(card: e_INFO_CARD_ONLINE_GW_MSG) -> bytes:
        data = bytearray()
        data.append(card.cmd)
        data.append(card.status & 0xFF)
        data.append(card.rssi & 0xFF)

        name_bytes = card.operator_name.encode("utf-8")
        data.append(len(name_bytes))
        data.extend(name_bytes)

        data.extend(card.ip)
        data.extend(card.netmask)
        data.extend(card.gateway)
        data.extend(card.dns1)
        data.extend(card.version)

        return bytes(data)