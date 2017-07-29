#!/usr/bin/env python
import re
import os
import sys

#--------------------------------------------------------#
# Name: string2opcode                                    #
# Author: Amonsec                                        #
# Published: Jul 2 2017                                  #
# Python version: 2.7                                    #
#--------------------------------------------------------#

# Colorz
RED = "\x1B[1;31m"
BLU = "\x1B[1;34m"
GRE = "\x1B[1;32m"
RST = "\x1B[0;0;0m"

# lambda
info_message = lambda x: '{}[*]{} {}'.format(BLU, RST, x)
suce_message = lambda x: '{}[+]{} {}'.format(GRE, RST, x)
erro_message = lambda x: '{}[-]{} {}'.format(RED, RST, x)

# Main code
print info_message('Convert string to Opcode (v1.0)')
print info_message('Author {}Amonsec{}\n'.format(RED, RST))
if len(sys.argv) < 3 :
    print info_message('Usage: python {} [options] <values>'.format(sys.argv[0]))
    print info_message('Options: ')
    print '\t -f; --file\t Convert string(s) in a given file'
    print '\t -r; --raw\t Convert the given string in argument'
    print ''
    print info_message('Usage Examples: ')
    print '\t python {} --file test.txt'.format(sys.argv[0])
    print '\t python {} --file /root/Desktop/test.txt'.format(sys.argv[0])
    print '\t python {} --raw lulzing'.format(sys.argv[0])
    print '\t python {} --raw \'Opcode to OP\''.format(sys.argv[0])
    print ''
    print info_message('Badchars Examples: ')
    print '\t Badchars: \\x41'
    print '\t Badchars: \\x00\\x0a\\x0d\\x20'
    sys.exit() 

# Get the string to convert into opcode
try:
    if sys.argv[1] in ('-r', '--raw'):
        message = sys.argv[2]
    elif sys.argv[1] in ('-f', '--file'):
        file = sys.argv[2]
        if os.path.isfile(file):
            print info_message('File found')
        else:
            print erro_message('File not found')
            sys.exit()
        data = open(file, 'r')
        message = data.read()
        data.close()
    else:
        while True:
            message = raw_input('Your string: ')
            if len(message) != 0:
                break

except KeyboardInterrupt:
    print '\nHave Fun 1337\n'
    sys.exit()

# Badchars :-)
try:
    badchar = raw_input("{}[*]{} Badchars: ".format(BLU, RST))
    badchars = badchar.split('\\x')
    badchars.pop(0)

except KeyboardInterrupt:
    print '\nHave Fun 1337\n'
    sys.exit()

try:
    # Convert to hexadecimal and add spaces
    hexchain = ''
    strings = message.split(' ')
    counter = 1
    maximum = len(strings)
    for string in strings:
        hexchain += string.encode('hex')
        if counter != maximum:
            hexchain +=  '20'
            counter += 1

    # Add useless space hex characters till we have a height divider
    while True:
        if (len(hexchain) % 8 != 0):
            hexchain += '20'
        else:
            break
    
    # Split the hexchain each 2 characters
    # And reverse the chain
    reverse = ''
    for x in (re.findall('..', hexchain))[::-1]:
        reverse += x

    print suce_message('Hexchain lenght: {} bytes'.format(len(hexchain)))
    print suce_message('Hexchain: :\n\n{}\n'.format(reverse))
    print suce_message('Your Opcode: \n')

    # Detect in badchars are present
    detected = []
    havebads = False
    for y in re.findall('........', reverse):
        decode = y.decode('hex')

        # Red diplay for founded badchars
        for b in badchars:
            for z in re.findall('..', reverse):
                if str(b) == str(z):
                    if not b in detected:
                        detected.append(b)
                    havebads = True
                    y = re.sub(b, RED+b+RST, y)

        # Print the opcode
        decode = re.sub('\\n', '\\\\n', decode)
        decode = re.sub('\\r', '\\\\r', decode)
        print 'push 0x{} ; {}'.format(y, decode)

    # Badchars report
    print ''
    if havebads:
        i = ''
        for d in detected:
            i += '\\x{}'.format(d)
        print erro_message('Badchars detected: {}'.format(i))
    else:
        print suce_message('No Badchars detected')

    print info_message('Have Fun 1337')
    sys.exit()

except KeyboardInterrupt:
    print info_message('\nHave Fun 1337\n')
    sys.exit()
