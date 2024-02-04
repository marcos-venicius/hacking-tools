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

class Parser:
    def __init__(self, byts):
        self.byts = byts

    def __parse_destination_mac(self):
        return ':'.join([byt.upper() for byt in self.byts[0:6]])

    def __parse_origin_mac(self):
        return ':'.join([byt.upper() for byt in self.byts[6:12]])

    def __parse_protocol_type(self):
        pt = {'0800': 'IPv4', '0806': 'ARP'}

        return pt[''.join(self.byts[12:14])]

    def __parse_arp_hardware_type(self):
        ht = {'0001': 'Ethernet'}

        return ht[''.join(self.byts[14:16])]

    def __parse_arp_protocol_type(self):
        pt = {'0800': 'IPv4'}

        return pt[''.join(self.byts[16:18])]
    
    def __parse_arp_hardware_size(self):
        return int('0x' + self.byts[18], 16)

    def __parse_arp_protocol_size(self):
        return int('0x' + self.byts[19], 16)

    def __parse_arp_opcode(self):
        return int('0x' + ''.join(self.byts[20:22]), 16)

    def __parse_arp_sender_mac(self):
        return ':'.join([b.upper() for b in self.byts[22:28]])

    def __parse_arp_sender_ip(self):
        return '.'.join([str(int('0x' + b, 16)) for b in self.byts[28:32]])

    def __parse_arp_target_mac(self):
        return ':'.join([b.upper() for b in self.byts[32:38]])

    def __parse_arp_target_ip(self):
        return '.'.join([str(int('0x' + b, 16)) for b in self.byts[38:42]])

    def __parse_arp_padding(self):
        return ''.join([i.upper() for i in self.byts[42:]])

    def parse(self):
        result = {
            'Ethernet': {
                'destination_mac': self.__parse_destination_mac(),
                'origin_mac': self.__parse_origin_mac(),
                'protocol': self.__parse_protocol_type(),
            }
        }

        if result['Ethernet']['protocol'] == 'ARP':
            result['ARP'] = {}
            result['Ethernet']['padding'] = self.__parse_arp_padding()
            result['ARP']['hardware_type'] = self.__parse_arp_hardware_type()
            result['ARP']['protocol_type'] = self.__parse_arp_protocol_type()
            result['ARP']['hardware_size'] = self.__parse_arp_hardware_size()
            result['ARP']['protocol_size'] = self.__parse_arp_protocol_size()
            result['ARP']['opcode'] = self.__parse_arp_opcode()
            result['ARP']['sender_mac_address'] = self.__parse_arp_sender_mac()
            result['ARP']['sender_ip_address'] = self.__parse_arp_sender_ip()
            result['ARP']['target_mac_address'] = self.__parse_arp_target_mac()
            result['ARP']['target_ip_address'] = self.__parse_arp_target_ip()

        return result

def display(byts):
    parser = Parser(byts)

    data = parser.parse()

    protocol = data['Ethernet']['protocol']

    print('Ethernet:')
    print(f'  Destination MAC Address:  {data["Ethernet"]["destination_mac"]}')
    print(f'  Source MAC Address:       {data["Ethernet"]["origin_mac"]}')
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
    else:
        print('Unimplemented protocol')


bytesfile = params()
byts = read_bytes(bytesfile)

display(byts)

