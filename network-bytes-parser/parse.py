#!/usr/bin/env python3

import sys

def params():
    if len(sys.argv) != 2:
        print('Usage: ./main.py <bytes-file>')
        exit(1)

    return sys.argv[1]

def read_bytes(file):
    with open(file, 'r') as f:
        lines = f.readlines()
        lines = [line.split(' ') for line in lines]
        result = []

        for line in lines:
            for byt in line:
                byt = byt.replace('\n', '')
                if byt: result.append(byt)

        return result

class Ethernet:
    def __init__(self, byts):
        self.byts = byts[0:14]

    def __parse_destination_mac(self):
        return ':'.join([byt.upper() for byt in self.byts[0:6]])

    def __parse_source_mac(self):
        return ':'.join([byt.upper() for byt in self.byts[6:12]])

    def __parse_protocol(self):
        pt = {'0800': 'IPv4', '0806': 'ARP'}

        return pt[''.join(self.byts[12:])]

    def parse(self):
        return {
            'destination_mac': self.__parse_destination_mac(),
            'source_mac': self.__parse_source_mac(),
            'protocol': self.__parse_protocol(),
            'padding': ''
        }

class ARP:
    def __init__(self, byts):
        self.byts = byts[14:]

    def __parse_hardware_type(self):
        ht = {'0001': 'Ethernet'}

        return ht[''.join(self.byts[:2])]

    def __parse_protocol_type(self):
        pt = {'0800': 'IPv4'}

        return pt[''.join(self.byts[2:4])]
    
    def __parse_hardware_size(self):
        return int('0x' + self.byts[4], 16)

    def __parse_protocol_size(self):
        return int('0x' + self.byts[5], 16)

    def __parse_opcode(self):
        return int('0x' + ''.join(self.byts[6:8]), 16)

    def __parse_sender_mac(self):
        return ':'.join([b.upper() for b in self.byts[8:14]])

    def __parse_sender_ip(self):
        return '.'.join([str(int('0x' + b, 16)) for b in self.byts[14:18]])

    def __parse_target_mac(self):
        return ':'.join([b.upper() for b in self.byts[18:24]])

    def __parse_target_ip(self):
        return '.'.join([str(int('0x' + b, 16)) for b in self.byts[24:28]])

    def __parse_padding(self):
        return ''.join([i.upper() for i in self.byts[28:]])

    def parse(self):
        return {
            'padding': self.__parse_padding(),
            'hardware_type': self.__parse_hardware_type(),
            'protocol_type': self.__parse_protocol_type(),
            'hardware_size': self.__parse_hardware_size(),
            'protocol_size': self.__parse_protocol_size(),
            'opcode': self.__parse_opcode(),
            'sender_mac_address': self.__parse_sender_mac(),
            'sender_ip_address': self.__parse_sender_ip(),
            'target_mac_address': self.__parse_target_mac(),
            'target_ip_address': self.__parse_target_ip()
        }

class IPv4:
    def __init__(self, byts):
        self.byts = byts[14:]

    def __parse_source_ip_address(self):
        return '.'.join([str(int('0x' + i, 16)) for i in self.byts[11:15]])

    def parse(self):
        return {
            'source_ip_address': self.__parse_source_ip_address()
        }

class Parser:
    def __init__(self, byts):
        self.byts = byts

    def parse(self):
        eth = Ethernet(self.byts).parse()

        result = {
            'Ethernet': eth
        }

        if eth['protocol'] == 'ARP':
            arp = ARP(byts).parse()
            result['ARP'] = arp
            result['Ethernet']['padding'] = arp['padding']
        elif eth['protocol'] == 'IPv4':
            ipv4 = IPv4(self.byts).parse()
            result['IPv4'] = ipv4

        return result

def display(byts):
    parser = Parser(byts)

    data = parser.parse()

    protocol = data['Ethernet']['protocol']

    print('Ethernet:')
    print(f'  Destination MAC Address:  {data["Ethernet"]["destination_mac"]}')
    print(f'  Source MAC Address:       {data["Ethernet"]["source_mac"]}')
    print(f'  Protocol:                 {protocol}')
    print(f'  Padding:                  {data["Ethernet"]["padding"]}')
    print()
    print(f'  {protocol}:')

    if protocol == 'ARP':
        print(f'    Hardware Type:          {data[protocol]["hardware_type"]}')
        print(f'    Protocol Type:          {data[protocol]["protocol_type"]}')
        print(f'    Hardware Size:          {data[protocol]["hardware_size"]}')
        print(f'    Protocol Size:          {data[protocol]["protocol_size"]}')
        print(f'    Opcode:                 {data[protocol]["opcode"]}')
        print(f'    Sender MAC Address:     {data[protocol]["sender_mac_address"]}')
        print(f'    Sender IP Address:      {data[protocol]["sender_ip_address"]}')
        print(f'    Target MAC Address:     {data[protocol]["target_mac_address"]}')
        print(f'    Target IP Address:      {data[protocol]["target_ip_address"]}')
    elif protocol == 'IPv4':
        print(f'    Source IP Address:      {data[protocol]["source_ip_address"]}')
    else:
        print('Unimplemented protocol')


bytesfile = params()
byts = read_bytes(bytesfile)

display(byts)

