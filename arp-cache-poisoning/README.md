# ARP Cache poisoning tool

This tool use the scapy packet from python to execute an attack
called ARP Cache Poisoning.

**This script is for education purposes only! We are not responsible for misuse of the tool**

To make this works, you basically need the IP of your gateway and you can grab it with `route -n` will be at destination `0.0.0.0`
and the ip of the victim.

You need to execute this script as sudo because he will try to get your mac address to use in the process.

### Executing the script

Example

```bash
sudo ./attack.py <victim-ip> <gateway-ip>
```

The first parameter is the gateway and the last parameter is the victim machine ip.

### Improving

You will notice that when you ran the script and the ARP cache was poisoned, the victim machine can't access the internet.

And that's fine, because your attack machine is not a router.

Buuuuttt, we can make it be one!

To do this, we just need to enable the IP Forwarding on your machine.

```bash
sudo su
```

```bash
echo 1 > /proc/sys/net/ipv4/ip_forward
```

* And, open the file `/etc/sysctl.conf`
* Search for `#net.ipv4.ip_forward=0`
* Umcomment if is commented
* Change the number `0` to `1` and boom.

Now the victim can access the internet.

And, you can see the traffic by using wireshark for example.

### Stopping

To stop the script just press `CTRL-C`, this will restore the ARP cache too.

Now, restore your ip forwarding:

```bash
sudo su
```

```bash
echo 0 > /proc/sys/net/ipv4/ip_forward
```

* And, open the file `/etc/sysctl.conf`
* Search for `net.ipv4.ip_forward=1`
* Change the number `1` to `0`.

