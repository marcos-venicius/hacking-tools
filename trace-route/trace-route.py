#!/usr/bin/env python3

from scapy.all import IP, ICMP, sr1

def ip_is_valid(ip):
    import re

    pattern = re.compile("\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}")
    return pattern.match(ip)

def author():
    print("""
████████╗██████╗  █████╗  ██████╗███████╗    ██████╗  ██████╗ ██╗   ██╗████████╗███████╗
╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██╔════╝    ██╔══██╗██╔═══██╗██║   ██║╚══██╔══╝██╔════╝
   ██║   ██████╔╝███████║██║     █████╗      ██████╔╝██║   ██║██║   ██║   ██║   █████╗  
   ██║   ██╔══██╗██╔══██║██║     ██╔══╝      ██╔══██╗██║   ██║██║   ██║   ██║   ██╔══╝  
   ██║   ██║  ██║██║  ██║╚██████╗███████╗    ██║  ██║╚██████╔╝╚██████╔╝   ██║   ███████╗
   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚══════╝    ╚═╝  ╚═╝ ╚═════╝  ╚═════╝    ╚═╝   ╚══════╝
                                                                                        
by @marcos-venicius, https://github.com/marcos-venicius
""")

def params():
    import sys

    if len(sys.argv) != 2:
        print('Usage: sudo ./trace-route.py <ip>')
        exit(1)

    if not ip_is_valid(sys.argv[1]):
        print('\033[1;31m[!] Invalid IP address\033[0m')
        exit(1)

    return sys.argv[1]

def is_sudo():
    import os

    return os.geteuid() == 0

def trace(ttl, ip):
    ip = IP(
        dst=ip,
        ttl=ttl
    )

    icmp = ICMP()

    return sr1(ip / icmp, verbose=False, timeout=1)

if not is_sudo():
    print('\033[1;31m[!] You should run as sudo\033[0m')
    exit(1)

ip = params()

author()

print('\033[0;36m[*] Press ctrl+c when you want to stop\033[0m\n')
print('\033[1;37mTracing route...\033[0m\n')

try:
    found, ttl, counter = set(), 1, 0

    while True:
        res = trace(ttl, ip)

        if res:
            if res.src in found:
                break
            else:
                found.add(res.src)

            counter += 1

            print(f'[{str(counter).ljust(3, " ")}] {res.src}')

        ttl += 1

    print('\n\033[1;32m[+] Tracing finished\033[0m\n')
except:
    exit(0)
