#!/bin/bash

if [ -z "$1" ]; then
	echo "Usage: $0 <binary>"
	echo "Bye :)"
	exit
fi

echo "[+] Shellcode: "
echo ""; for i in `objdump -d $1 | tr '\t' ' ' | tr ' ' '\n' | egrep '^[0-9a-f]{2}$' ` ; do echo -n "\x$i" ; done; echo ""; echo ""
