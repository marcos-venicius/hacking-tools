#!/bin/bash

if [ "$1" == "--help" ] || [ "$1" == "" ]; then
  echo -e "\033[1;33m
Usage: $0 <network>
Example: $0 10.0.0.1\033[0m"
  exit 0
fi

if [ "$(echo $1 | grep -oP  "\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}")" == "" ]; then
  echo -e "\033[1;31mInvalid network"
  exit 1
fi

base_host=$(echo $1 | grep -oP "\d{1,3}.\d{1,3}.\d{1,3}")

echo -e "\033[2;32m
███████╗ ██████╗ ██████╗ ███████╗████████╗███████╗
██╔════╝██╔════╝██╔═══██╗██╔════╝╚══██╔══╝██╔════╝
███████╗██║     ██║   ██║███████╗   ██║   ███████╗
╚════██║██║     ██║   ██║╚════██║   ██║   ╚════██║
███████║╚██████╗╚██████╔╝███████║   ██║   ███████║
╚══════╝ ╚═════╝ ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝

\033[1;37mBy https://github.com/marcos-venicius

\033[0m
Scanning Hosts:

"

hosts=()
found=0
max=254
range=$(seq 1 $max)

for i in $range; do
  percentage=$(($i * 100 / $max))
  echo -ne "Scanning... $percentage%\tFound $found\r"

  host=$base_host.$i
  output=$(ping $host -c 1 -s 1 -W 1 -q -n)

  if grep -q "1 received" <<< $output; then
    ((found++))
    hosts+=($host)
  fi
done

echo -e "\n\n\033[1;37mHosts found:\n"

for host in "${hosts[@]}"; do
  echo -e "\033[1;32m  $host\033[0m"
done
