import socket
from scapy.all import *
import math

SRC_PORT = 65000

SYN           = 0x02
trios_tracker = {}

def is_done(packet):
    """
    function applied to each packet to determine
    if we have to stop the capture after this packet.
    """
    total_trios = packet[TCP].ack
    return len(trios_tracker) == total_trios

def handle_packets(packet):
    if not packet.haslayer(TCP):
        return
    if packet[TCP].flags != SYN:
        return
    trio_idx                = packet[TCP].seq
    trios_tracker[trio_idx] = packet[TCP].reserved
    
def assemble_message():
    message_in_bits = 0
    max_trio_idx = max(trios_tracker.keys())
    for trio_idx in range(max_trio_idx, -1, -1):
        message_in_bits = (message_in_bits << 3) + trios_tracker[trio_idx]
    nof_bits = len(bin(message_in_bits)) - 2
    message_in_bytes = message_in_bits.to_bytes(math.ceil(nof_bits/8), 'big')
    return message_in_bytes.decode('latin-1')

def receive_message(port: int) -> str:
    """Receive *hidden* messages on the given TCP port.

    As Winston sends messages encoded over the TCP metadata, re-implement this
    function so to be able to receive the messages correctly.

    Notes:
    1. Use `SRC_PORT` as part of your implementation.
    """

    sniff(filter = 'src port %d'%SRC_PORT, prn=handle_packets, stop_filter=is_done)

    #assemble the message
    return assemble_message()

def main():
    # WARNING: DO NOT MODIFY THIS FUNCTION!
    message = receive_message(1984)
    print('received: %s' % message)


if __name__ == '__main__':
    main()
