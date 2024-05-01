#!./venv/bin/python3.10

from question import Question
import os
from tracer import Tracer
from validations import ip_is_valid
from geolocation import geolocate, display_geolocation
import argparse

progname = os.path.basename(__file__)

parser = argparse.ArgumentParser(
    prog=progname,
    description='Trace route and IP lookup',
    epilog=f'{progname} 93.184.215.14'
)

parser.add_argument('ip', help='IP to trace')
parser.add_argument('--max-ttl', type=int, default=30, help='Set the max number of hops (max TTL reached). default is 30')
parser.add_argument('--no-cache', action='store_true', default=False, help='Force the program to not use cache')

args = parser.parse_args()

if not ip_is_valid(args.ip):
    print('\033[1;31m[!] Invalid IP address\033[0m')
    exit(1)


if os.geteuid() != 0:
    print('\033[1;31m[!] You should run as sudo\033[0m')
    exit(1)

print("""\033[1;32m
████████╗██████╗  █████╗  ██████╗███████╗    ██████╗  ██████╗ ██╗   ██╗████████╗███████╗
╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██╔════╝    ██╔══██╗██╔═══██╗██║   ██║╚══██╔══╝██╔════╝
   ██║   ██████╔╝███████║██║     █████╗      ██████╔╝██║   ██║██║   ██║   ██║   █████╗  
   ██║   ██╔══██╗██╔══██║██║     ██╔══╝      ██╔══██╗██║   ██║██║   ██║   ██║   ██╔══╝  
   ██║   ██║  ██║██║  ██║╚██████╗███████╗    ██║  ██║╚██████╔╝╚██████╔╝   ██║   ███████╗
   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚══════╝    ╚═╝  ╚═╝ ╚═════╝  ╚═════╝    ╚═╝   ╚══════╝
                                                                                        
\033[1;36mby @marcos-venicius, https://github.com/marcos-venicius\033[0m
""")

print('\033[0;36m[*] Press ctrl+c when you want to stop\033[0m\n')

tracer = Tracer(args.no_cache, args.max_ttl, args.ip)

results = tracer.trace()

print('\n\033[1;32m[+]\033[0m Tracing finished\n')

question = Question({ 'y': 'yes', 'n': 'no' })

response = question.ask("You want to loopkup the IP's location? ")

print()

if response == 'n':
    print('Bye')
    exit(0)

for ttl, ip in results:
    if ip:
        result = geolocate(ip, args.no_cache)
        print('\033[1;32m' + str(ttl).rjust(3, ' ') + ' \033[0m' + ip)
        display_geolocation(result)
    else:
        print('\033[1;31m' + str(ttl).rjust(3, ' ') + ' \033[0m*')
