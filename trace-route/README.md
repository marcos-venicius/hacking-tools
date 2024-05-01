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
* The default MAX_TTL(number of HOPS) is 30

Example:

```bash
sudo ./trace-route.py 10.0.0.4
```

if you wanna change the max TTL, you can use like:

```bash
sudo MAX_TTL=40 ./trace-route.py 10.0.0.4
```
