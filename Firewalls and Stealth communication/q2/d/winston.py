import socket
from scapy.all import *
import math

SRC_PORT = 65000


def send_message(ip: str, port: int):
    """Send a *hidden* message to the given ip + port.

    Julia expects the message to be hidden in the TCP metadata, so re-implement
    this function accordingly.

    Notes:
    1. Use `SRC_PORT` as part of your implementation.
    """
    message_as_integer = int.from_bytes(b'I love you', 'big')
    total_trios = math.ceil(len(bin(message_as_integer)) / 3)
    for idx in range(total_trios):
        curr_trio = (message_as_integer >> (3*idx)) & 0b111
        syn = IP(dst=ip) / TCP(sport=SRC_PORT, dport=port, flags='S', reserved = curr_trio, seq=idx, ack=total_trios)
        send(syn)


def main():
    # WARNING: DO NOT MODIFY THIS FUNCTION!
    send_message('127.0.0.1', 1984)


if __name__ == '__main__':
    main()
