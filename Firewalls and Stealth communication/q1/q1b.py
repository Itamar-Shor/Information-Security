import time
import os
from scapy.all import *


WINDOW = 60
MAX_ATTEMPTS = 15

SYN = 0x02
# Initialize your data structures here
# TODO: Initialize your data structures

class Sync_manager():
    def __init__(self, window=WINDOW, max_attempts=MAX_ATTEMPTS):
        self.tracker        = {}
        self.window         = window
        self.max_attempts   = max_attempts

    def process_sync_req(self, ip, toa) -> bool:
        """
        updates the tracker dict with the new sync request.
        return True if there are 15 (or more) sync req from the same IP addr.
        return False otherwise.
        """
        if ip in self.tracker:
            self.tracker[ip].append(toa + self.window)
            self.slide_window(ip=ip, curr_time=toa)
            if len(self.tracker[ip]) > self.max_attempts:
                return True
        else:
            self.tracker[ip] = [toa + self.window]
        return False
    
    def slide_window(self, ip, curr_time):
        """
        update the self.tracker to contain only valid req (i.e. req that havn't been timed out).
        """
        idx = 0
        while idx < len(self.tracker[ip]) and curr_time > self.tracker[ip][idx]:
            idx += 1
        self.tracker[ip] = self.tracker[ip][idx:] # deleting syns that doesn't fit in the curr window
    
    def remove(self, ip):
        if ip in self.tracker:
            self.tracker.pop(ip)

sync_manager = Sync_manager()
blocked = set()  # We keep blocked IPs in this set


def on_packet(packet):
    """This function will be called for each packet.

    Use this function to analyze how many packets were sent from the sender
    during the last window, and if needed, call the 'block(ip)' function to
    block the sender.

    Notes:
    1. You must call block(ip) to do the blocking.
    2. The number of SYN packets is checked in a sliding window.
    3. Your implementation should be able to efficiently handle multiple IPs.
    """
    rcv_time = time.time()
    if not packet.haslayer(TCP) or not packet.haslayer(IP):
        return

    src_ip = packet[IP].src
    if is_blocked(src_ip) or packet[TCP].flags != SYN:
        return
    # packet is SYN packet from non blocked ip!
    if sync_manager.process_sync_req(ip=src_ip, toa=rcv_time):
        block(src_ip)
        sync_manager.remove(ip=src_ip)
    

def generate_block_command(ip: str) -> str:
    """Generate a command that when executed in the shell, blocks this IP.

    The blocking will be based on `iptables` and must drop all incoming traffic
    from the specified IP."""

    block_cmd = "iptables -A INPUT -s {} -j DROP".format(ip)
    return block_cmd

def block(ip):
    # WARNING: DO NOT MODIFY THIS FUNCTION!
    os.system(generate_block_command(ip))
    blocked.add(ip)


def is_blocked(ip):
    # WARNING: DO NOT MODIFY THIS FUNCTION!
    return ip in blocked


def main():
    # WARNING: DO NOT MODIFY THIS FUNCTION!
    sniff(prn=on_packet)


if __name__ == '__main__':
    main()
