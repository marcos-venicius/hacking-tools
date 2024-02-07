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
        return '.'.join([str(int('0x' + i, 16)) for i in self.byts[12:16]])

    def __parse_destination_ip_address(self):
        return '.'.join([str(int('0x' + i, 16)) for i in self.byts[16:20]])

    def __parse_protocol(self):
        p = { 6: 'TCP' }
        return p[int(self.byts[9], 16)]

    def __parse_ihl(self):
        return int(self.byts[0][1], 16) * 4

    def parse(self):
        return {
            'source_ip_address': self.__parse_source_ip_address(),
            'destination_ip_address': self.__parse_destination_ip_address(),
            'protocol': self.__parse_protocol(),
            'ihl': self.__parse_ihl(),
            'payload': self.byts[self.__parse_ihl():]
        }

class TCP:
    def __init__(self, byts):
        self.byts = byts

    def __parse_source_port(self):
        return int(''.join(self.byts[0:2]), 16)

    def __parse_destination_port(self):
        return int(''.join(self.byts[2:4]), 16)

    def __parse_flags(self):
        flags_d = {32: 'URG', 16: 'ACK', 8: 'PSH', 4: 'RST', 2: 'SYN', 1: 'FIN'}
        flags_a = [32, 16, 8, 4, 2, 1]

        flags = int(self.byts[13], 16)
        f = []

        for i in flags_a:
            if i <= flags:
                f.append(flags_d[i])
                flags -= i

        return ', '.join(reversed(f))

    def __parse_data_offset(self):
        return int(self.byts[12][0], 16)

    def __parse_data(self):
        return bytes.fromhex(''.join(self.byts[24+self.__parse_data_offset():])).decode('ascii')

    def parse(self):
        return {
            'source_port': self.__parse_source_port(),
            'destination_port': self.__parse_destination_port(),
            'flags': self.__parse_flags(),
            'data_offset': self.__parse_data_offset(),
            'data': self.__parse_data()
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

            if ipv4['protocol'] == 'TCP':
                ipv4['TCP'] = TCP(ipv4['payload']).parse()

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
        print(f'    IHL:                    {data[protocol]["ihl"]}')
        print(f'    Source IP Address:      {data[protocol]["source_ip_address"]}')
        print(f'    Destination IP Address: {data[protocol]["destination_ip_address"]}')
        print(f'    Protocol:               {data[protocol]["protocol"]}')
        print()
        print(f'    {data[protocol]["protocol"]}:')

        if data[protocol]["protocol"] == "TCP":
            protocol = data[protocol][data[protocol]['protocol']]
            print(f'        Source Port:        {protocol["source_port"]}')
            print(f'        Destination Port:   {protocol["destination_port"]}')
            print(f'        Flags:              {protocol["flags"]}')
            print(f'        Data Offset:        {protocol["data_offset"]}')
            print(f'        Data:               {protocol["data"]}')
        else:
            print('        Unimplemented protocol')
    else:
        print('Unimplemented protocol')


bytesfile = params()
byts = read_bytes(bytesfile)

display(byts)

