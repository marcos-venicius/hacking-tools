# SCOSTS (Scan Hosts)

![Screenshot 2024-02-08 072758](https://github.com/marcos-venicius/hacking-tools/assets/94018427/87204b97-8a0d-4eb6-b772-1ded8925beb6)

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
