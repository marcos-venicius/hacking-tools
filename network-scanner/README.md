# SCOSTS (Scan Hosts)

Under the hood, the comand that is ran:

```bash
ping <host> -c 1 -s 1 -W 1 -q -n
```

But, in an automated way.

## Running

```bash
./scosts.sh --help # to get help
```

```bash
./scosts.sh 10.0.0.1 # for example of a network
```
