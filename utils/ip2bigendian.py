#!/usr/bin/python
import sys

if len(sys.argv) < 2:
	print info_message('Usage: python {} <string>'.format(sys.argv[0]))
	sys.exit(0)

ip = sys.argv[1]

b = ''
for x in ip.split('.')[::-1]:
	hexchain =  hex(int(x)).split('x')[1]
	if len(hexchain) < 2:
		b += '0' + hexchain
	else:
		b += hexchain

print 'push 0x' + b + ' ; ' + ip

