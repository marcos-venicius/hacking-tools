# Trace Route

![Screenshot from 2024-04-30 21-35-24](https://github.com/marcos-venicius/hacking-tools/assets/94018427/be36b0d4-2b18-4ebc-a101-7679c8a21a6a)

![Screenshot from 2024-04-30 21-35-35](https://github.com/marcos-venicius/hacking-tools/assets/94018427/e9c4ae50-c435-42cb-879a-1bf23c7d328d)

Basically the concept works using the TTL parameter of the IP protocol.

When you send a packet using the IP protocol, automatically it receives a default TTL (Time To Live) value,
this TTL may be 64, 128, 255, or any other customized by a user.

**What is the purpose of the TTL?**

When a packet is created and sent with a TTL 10, for example, the router receives this packet and decrements your value by 1
meaning that the next router that get this packet will reach the TTL value being 9 and this process
happens every time that this packets pass by a new router, this process is called HOP.

So, when the TTL reachs 0 the router returns a ICMP response with the type 11 and code 0, meaning that
this packet has expired, so we can get the router ip.

By incrementing the TTL value one by one (starting at 1) we can keep track the routers in the packet transmition path.

## Running

* This script should run as sudo
* This script needs a parameter that is the target you want to trace the route
    * it cannot be a domain, to transform the domain in a IP you can use my [DNS Resolver tool](../dns-resolver/) that is free.
* The default MAX_TTL(number of HOPS) is 30. If you wanna change this, use the flag `--max-ttl` and pass your own value.
* The program will cache the results by default and if has data in cache will get from there. If you don't wanna this behavior, use the flag `--no-cache`
* You will be asked (after the route trace) if you want to lookup for the IP's geolocation, you wanna make this yes at startup time, pass the flag `--yes` to don't ask questions

Example:

```bash
usage: trace-route.py [-h] [--max-ttl MAX_TTL] [--no-cache] [-y] ip

Trace route and IP lookup

positional arguments:
  ip                 IP to trace

options:
  -h, --help         show this help message and exit
  --max-ttl MAX_TTL  Set the max number of hops (max TTL reached). default is 30
  --no-cache         Force the program to not use cache
  -y, --yes          Don't ask questions, just continue

trace-route.py 93.184.215.14
```

