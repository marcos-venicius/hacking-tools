#!/usr/bin/env python3

from question import Question
import os
from tracer import Tracer
from geolocation import geolocate, display_geolocation

def ip_is_valid(ip):
    import re

    pattern = re.compile("\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}")
    return pattern.match(ip)

def author():
    print("""\033[1;32m
████████╗██████╗  █████╗  ██████╗███████╗    ██████╗  ██████╗ ██╗   ██╗████████╗███████╗
╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██╔════╝    ██╔══██╗██╔═══██╗██║   ██║╚══██╔══╝██╔════╝
   ██║   ██████╔╝███████║██║     █████╗      ██████╔╝██║   ██║██║   ██║   ██║   █████╗  
   ██║   ██╔══██╗██╔══██║██║     ██╔══╝      ██╔══██╗██║   ██║██║   ██║   ██║   ██╔══╝  
   ██║   ██║  ██║██║  ██║╚██████╗███████╗    ██║  ██║╚██████╔╝╚██████╔╝   ██║   ███████╗
   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚══════╝    ╚═╝  ╚═╝ ╚═════╝  ╚═════╝    ╚═╝   ╚══════╝
                                                                                        
\033[1;36mby @marcos-venicius, https://github.com/marcos-venicius\033[0m
""")

def params():
    import sys

    if len(sys.argv) != 2:
        print('Usage: sudo ./trace-route.py <ip>')
        exit(1)

    if sys.argv[1] in ('--help', '-h'):
        print('Usage: sudo ./trace-route.py <ip>')
        print('[env] MAX_TTL\t\tSet the max number of hops (max TTL to be reached). Default is 30')
        print('[env] NO_CACHE\t\tForce the program not use the cache, default is FALSE. options: TRUE | FALSE')
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

def no_cache():
    import os

    env = os.environ.get('NO_CACHE')

    if env == 'TRUE': return True
    if env == 'FALSE': return False
    if env is None: return False

    raise Exception('Invalid "NO_CACHE" env value')

if not is_sudo():
    print('\033[1;31m[!] You should run as sudo\033[0m')
    exit(1)

ip = params()
MAX_TTL = get_max_ttl()
NO_CACHE = no_cache()

author()

print('\033[0;36m[*] Press ctrl+c when you want to stop\033[0m\n')
print('\033[1;37mTracing route...\033[0m\n')

tracer = Tracer(NO_CACHE, MAX_TTL, ip)

results = tracer.trace()

print('\n\033[1;37m[+] Tracing finished\033[0m\n')

question = Question({ 'y': 'yes', 'n': 'no' })

response = question.ask('You want to track the location? ')

if response == 'y':
    print()

    for ttl, ip in results:
        if ip:
            result = geolocate(ip)
            print('\033[1;32m' + str(ttl).rjust(3, ' ') + ' \033[0m' + ip)
            display_geolocation(result)
        else:
            print('\033[1;31m' + str(ttl).rjust(3, ' ') + ' \033[0m*')
