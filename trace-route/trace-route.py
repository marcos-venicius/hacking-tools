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

    if sys.argv[1] == '--help':
        print('Usage: sudo ./trace-route.py <ip>')
        print('[env] MAX_TTL\t\tSet the max number of hops (max TTL to be reached). Default is 30')
        exit(0)

    if not ip_is_valid(sys.argv[1]):
        print('\033[1;31m[!] Invalid IP address\033[0m')
        exit(1)

    return sys.argv[1]

def is_sudo():
    import os

    return os.geteuid() == 0

def get_max_ttl():
    import os

    env = os.environ.get("MAX_TTL")

    if env is None:
        return 30

    if env.isnumeric() and int(env) >= 1:
        return int(env)

    return 30


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
MAX_TTL = get_max_ttl()

author()

print('\033[0;36m[*] Press ctrl+c when you want to stop\033[0m\n')
print('\033[1;37mTracing route...\033[0m\n')

try:
    found, ttl = set(), 1

    while True:
        res = trace(ttl, ip)

        if res:
            if res.src in found:
                break
            else:
                found.add(res.src)

            print(f'\033[1;32m[{str(ttl).ljust(3, " ")}] {res.src}\033[0m')
        else:
            print(f'\033[1;31m[{str(ttl).ljust(3, " ")}] *\033[0m')

        if ttl >= MAX_TTL:
            break

        ttl += 1

    print('\n\033[1;37m[+] Tracing finished\033[0m\n')
except:
    exit(0)
