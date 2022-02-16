import math
from scapy.all import *


LOVE = 'love'
unpersons = set()


def spy(packet):
    """Check for love packets and encrypted packets.

    For each packet containing the word 'love', or a packed which is encrypted,
    add the sender's IP to the `unpersons` set.

    Notes:
    1. Use the global LOVE as declared above.
    """
    if not packet.haslayer(TCP) or not packet.haslayer(IP) or not packet.haslayer(Raw):
        return
    payload = packet[Raw].load.decode("latin-1")
    distribution = [float(payload.count(c)) / len(payload) for c in set(payload)]
    entropy = -sum(p * math.log(p) / math.log(2.0) for p in distribution)

    if LOVE in payload or entropy > 3:
        unpersons.add(packet[IP].src)


def shannon_entropy(string: str) -> float:
    # WARNING: DO NOT MODIFY THIS FUNCTION!
    distribution = [float(string.count(c)) / len(string)
                    for c in set(string)]
    return -sum(p * math.log(p) / math.log(2.0) for p in distribution)


def main():
    # WARNING: DO NOT MODIFY THIS FUNCTION!
    sniff(prn=spy)


if __name__ == '__main__':
    main()
