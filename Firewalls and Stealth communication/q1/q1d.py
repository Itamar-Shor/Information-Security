from scapy.all import *

SYN = 0x02

def on_packet(packet):
    """Implement this to send a SYN ACK packet for every SYN.

    Notes:
    1. Use *ONLY* the `send` function from scapy to send the packet!
    """
    if not packet.haslayer(TCP) or not packet.haslayer(IP):
        return
    if packet[TCP].flags != SYN:
        return
    dst_port    = packet[TCP].dport
    src_port    = packet[TCP].sport
    src_ip      = packet[IP].src
    dst_ip      = packet[IP].dst
    ack_number  = packet[TCP].seq + 1
    seq_number  = packet[TCP].seq
    sa_packet = IP(src=dst_ip, dst=src_ip) / TCP(sport=dst_port, dport=src_port, flags='SA', ack=ack_number, seq=seq_number)
    send(sa_packet)

def main(argv):
    # WARNING: DO NOT MODIFY THIS FUNCTION!
    sniff(prn=on_packet)


if __name__ == '__main__':
    # WARNING: DO NOT MODIFY THIS FUNCTION!
    import sys
    sys.exit(main(sys.argv))
