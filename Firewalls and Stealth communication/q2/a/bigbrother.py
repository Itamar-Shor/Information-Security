from scapy.all import *


LOVE = 'love'
unpersons = set()


def spy(packet):
    """Check for love packets.

    For each packet containing the word 'love', add the sender's IP to the
    `unpersons` set.

    Notes:
    1. Use the global LOVE as declared above.
    """
    if not packet.haslayer(TCP) or not packet.haslayer(IP) or not packet.haslayer(Raw):
        return
    if LOVE in packet[Raw].load.decode("latin-1"):
        unpersons.add(packet[IP].src)

def main():
    # WARNING: DO NOT MODIFY THIS FUNCTION!
    sniff(prn=spy)


if __name__ == '__main__':
    main()
