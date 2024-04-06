#!/bin/bash

if [ -z "$1" ]; then
  echo -e "\033[1;31m[!]\033[1;37m Empty args. Example: ./zone-transfer.sh example.com\033[0m"
  exit 0
fi

ns=$(host -t ns "$1" | cut -d ' ' -f4 | sed s/\.$//)
success=()

for x in $ns; do
  echo -e "\033[1;36m[*]\033[1;37m $x\033[0m"
  result=$(host -l -a "$1" "$x")
  if grep -q "failed" <<< "$result"; then
    echo -e "    \033[1;31m[!]\033[1;37m failed\033[0m"
  else
    echo -e "    \033[1;32m[+]\033[1;37m success\033[0m"
    success+=($x)
  fi
done

if [ ${#success[@]} -eq 0 ]; then
  echo -e "\n\033[1;31m[-]\033[1;37m NOT VULNERABLE\033[0m\n"
  exit 0
fi

echo -e "\n\033[1;32m[+]\033[1;37m RESULTS\033[0m\n"

for n in ${success[@]}; do
  echo -e "\033[1;36m[*]\033[1;37m $n\033[0m"
  host -l -a $1 $n
  echo -e ""
done
