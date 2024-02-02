#!/usr/bin/env python3

from scapy.all import IP, DNS, DNSQR, UDP, RandShort, send, sr1

def params():
    import sys

    if len(sys.argv) != 2:
        print('Usage: sudo ./resolve-dns.py <domain>')
        exit(1)

    return sys.argv[1]

def decode_if_necessary(s):
    try:
        return s.decode()[:-1]
    except:
        return s

def author():
    print("""
██████╗ ███╗   ██╗███████╗    ██████╗ ███████╗███████╗ ██████╗ ██╗    ██╗   ██╗███████╗██████╗ 
██╔══██╗████╗  ██║██╔════╝    ██╔══██╗██╔════╝██╔════╝██╔═══██╗██║    ██║   ██║██╔════╝██╔══██╗
██║  ██║██╔██╗ ██║███████╗    ██████╔╝█████╗  ███████╗██║   ██║██║    ██║   ██║█████╗  ██████╔╝
██║  ██║██║╚██╗██║╚════██║    ██╔══██╗██╔══╝  ╚════██║██║   ██║██║    ╚██╗ ██╔╝██╔══╝  ██╔══██╗
██████╔╝██║ ╚████║███████║    ██║  ██║███████╗███████║╚██████╔╝███████╗╚████╔╝ ███████╗██║  ██║
╚═════╝ ╚═╝  ╚═══╝╚══════╝    ╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝ ╚══════╝ ╚═══╝  ╚══════╝╚═╝  ╚═╝

by @marcos-venicius, https://github.com/marcos-venicius
""")

def resolve(domain):
    ip = IP(
        dst='8.8.8.8'
    )

    udp = UDP(
        sport=RandShort(),
        dport=53
    )

    dns = DNS(
        rd=1,
        qd=DNSQR(
            qname=domain, qtype="A"
        )
    )

    pkt = ip / udp / dns

    ans = sr1(pkt, verbose=False)

    return ans.an[0].rdata

def main(domain):
    print(f'\033[1;37m[*] Making DNS resolution for {domain}\033[0m')

    ip = resolve(domain)
    ip = decode_if_necessary(ip)

    print(f'\033[1;32m[+] IP for {domain} is \033[1;36m"{ip}"\033[0m')

if __name__ == '__main__':
    author()
    main(params())
