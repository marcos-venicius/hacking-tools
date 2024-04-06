# Zone Transfer

Explore the vulnerability "AXFR Non-Authenticated".

You can just pass the domain, and that is it, you will see the output.

The script will search for all "NS" registers and try to execute a zone transfer, if success, it will show you the output containing the whole file.

```bash
./zone-transfer.sh example.com
```
