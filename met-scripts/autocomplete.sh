#!/bin/bash

## To change if needed
MSF_MET_PATH="/usr/share/metasploit-framework/scripts/meterpreter/"
####

echo "[*] Working & tested in Kali Linux, you probably need to change the"
echo "[*] meterpreter-framework path if you have another OS / configuration"
echo ""

function helper() {
  echo "[!] Simply add / remove custom scripts from root folder"
  echo "[!] Usage: $0 <option>"
  echo "[!] Options:"
  echo -e "\t-a, --add\t add all custom scripts"
  echo -e "\t-d, --delete\t delete all custom scripts"
  echo ""
  exit 1
}

function add_scripts() {
  for x in $(ls |grep .rb); do
    echo "Copying: $x"
    cp $x $MSF_MET_PATH
  done
}

function delete_scripts() {
  for x in $(ls |grep .rb); do
    if [ $(ls "$MSF_MET_PATH" |grep "$x" ) ]; then
      echo "Removing: $MSF_MET_PATH""$x"
      rm -f "$MSF_MET_PATH""$x"
    fi
  done
}

if [ -z "$1" ]; then
  helper
fi

case "$1" in
  -a ) add_scripts;;
  --add ) add_scripts;;
  -d ) delete_scripts;;
  --delete ) delete_scripts;;
  * ) helper;;
esac

echo ""
echo "[*] Down."
