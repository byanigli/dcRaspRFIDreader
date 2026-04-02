from domain.entites.e_UHF_RFID_TAG_READ import e_UHF_RFID_TAG_READ


class uhfRfidTagReadBuilder:

    @staticmethod
    def build(p: e_UHF_RFID_TAG_READ) -> bytes:
        data = bytearray()
        data.append(p.cmd)
        data.append(p.antennaNumber & 0xFF)
        data.append(p.tidLength & 0xFF)
        if (p.tid is not None):
         data.extend(p.tid)
        data.append(p.epcLength & 0xFF)
        data.extend(p.epc)
        data.append(p.rssi)
        data.extend(p.lastSeen)
        return bytes(data)
