# Network Bytes Parser

This tool has the purpose of learning more about the bytes on the network.

**This tool is not ready for production**

This tool can parse arp request based only on your bytes.

![network-bytes-parser](https://github.com/marcos-venicius/hacking-tools/assets/94018427/a237b9e1-c983-4b22-8fd1-b1f3e3f9794b)

## How it works?

This is the funny part!

Basically the bytes are in a sequence.

For example, the first 6 bytes are the destination MAC Address of the Ethernet protocol, and the next 6 bytes are the source MAC Address,
This will continue by getting the next and next bytes, but associating to the right field of the protocol.

So, based on the protocol that is passed (the protocol is after the origin mac "2 bytes"),
we can now apply different offset rules to get the correct values.

This tool, gets the bytes to the ARP protocol.

Here are the fields:

| Field name                            | From byte | To byte |
| ------------------------------------- | --------- | ------- |
| (Ethernet) Destination MAC Address    |  0        | 5       |
| (Ethernet) Source MAC Address         |  6        | 11      |
| (Ethernet) Protocol Type              |  12       | 13      |
| (ARP) Hardware Type                   |  14       | 15      |
| (ARP) Protocol Type                   |  16       | 17      |
| (ARP) Protocol Type                   |  16       | 17      |
| (ARP) Hardware Size                   |  18       | 18      |
| (ARP) Protocol Size                   |  19       | 19      |
| (ARP) Opcode                          |  20       | 21      |
| (ARP) Sender MAC Address              |  22       | 27      |
| (ARP) Sender IP Address               |  28       | 31      |
| (ARP) Target MAC Address              |  32       | 37      |
| (ARP) Target IP Address               |  38       | 41      |

## Running

```bash
./parse.py <file-with-bytes>
```

