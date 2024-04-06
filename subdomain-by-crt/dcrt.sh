#!/bin/bash

echo -e "\033[1;32m
██████╗  ██████╗██████╗ ████████╗
██╔══██╗██╔════╝██╔══██╗╚══██╔══╝
██║  ██║██║     ██████╔╝   ██║   
██║  ██║██║     ██╔══██╗   ██║   
██████╔╝╚██████╗██║  ██║   ██║   
╚═════╝  ╚═════╝╚═╝  ╚═╝   ╚═╝   
\033[1;37m
by https://github.com/marcos-venicius
\033[0m"

if [ -z "$1" ]; then
  echo -e "\033[1;31m[!]\033[0m missing 1 parameter. example: ./search domain.com"
  exit 1
fi

results=$(curl "https://crt.sh/?q=$1" --silent | egrep -v "Certificates|Criteria|crt.sh" | grep -oP ">([a-z-A-Z]|\.)+<" | cut -d '<' -f1 | cut -d '>' -f2 | sort | uniq | tr '\n' ' ')

for result in $results; do
  echo -e "\033[1;32m[*]\033[0m $result"
done
