#!/usr/bin/env python

import sys
import pefile
import argparse

__author__ = 'Amonsec'
__version__ = '1.0'

###
# Colors
###
_RED = '\x1b[1;31m'
_BLU = '\x1b[1;34m'
_GRE = '\x1b[1;32m'
_RST = '\x1b[0;0;0m'

header = '''
       ____            _    _         
      | __ ) _ __ ___ | | _| | ___ __ 
      |  _ \| '__/ _ \| |/ / |/ / '__|
      | |_) | | | (_) |   <|   <| |   
      |____/|_|  \___/|_|\_\_|\_\_|   {}{}{}
  Author: {}{}{}

  Like the ancient god, searching for code cave in a PE file.
  Alright.                                
'''.format(_GRE, __version__, _RST, _RED, __author__, _RST)

###
# Lambda
###
successMessage = lambda x: '{}[+]{} {}'.format(_GRE, _RST, x)
errorMessage = lambda x: '{}[-]{} {}'.format(_RED, _RST, x)
infoMessage = lambda x: '{}[*]{} {}'.format(_BLU, _RST, x)


def main(file, minimumCaveSize, targetedSection=None):

    try:
        binary = pefile.PE(file)
        fileDescriptor = open(file, 'rb')
    except IOError as error:
        print errorMessage(str(error))
        sys.exit()
    except pefile.PEFormatError as error:
        print errorMessage(str(error))
        sys.exit()

    # User input information
    print infoMessage('Binary name: {}'.format(file))
    print infoMessage('Minimum code cave size: {}\n'.format(minimumCaveSize))

    print infoMessage('Listing founded section ...')
    for section in binary.sections:
        message = '%s\t VA: 0x%08X\t VS: 0x%08X\tRS: 0x%08X \tCERW: 0x%08X' % (
            section.Name,
            section.VirtualAddress,
            section.Misc_VirtualSize,
            section.SizeOfRawData,
            section.Characteristics
        )
        print successMessage(message)

    # Retrieve all section from the PE Header
    print ''
    print infoMessage('Searching for code cave ...')
    for section in binary.sections:

        if targetedSection and section.Name != targetedSection:
            continue

        if section.SizeOfRawData == 0:
            continue

        report = ''
        space = 0
        count = 0

        # Open form the beginning
        fileDescriptor.seek(section.PointerToRawData, 0)

        # Start reading the file
        rawData = fileDescriptor.read(section.SizeOfRawData)

        for byte in rawData:
            count += 1
            if byte == '\x00':
                space += 1
            else:
                if space > int(minimumCaveSize):
                    # Raw Address = Pointer to Raw Data + Section offset - Cave offset
                    # Virtual Address = Module Entry Point + Section Virtual Address + Section offset - Cave offset
                    message = 'Total size: %d\tRA: 0x%08X\t VA: 0x%08X' % (
                        space,
                        section.PointerToRawData + count - space - 1,
                        0x00400000 + section.VirtualAddress + count - space - 1
                    )
                    report += successMessage(message) + '\n'

                # Reset
                space = 0

        if report != '':
            print infoMessage('Code cave found in the {} section'.format(section.Name))
            print report

    # Close both the file descriptor and the PE file
    fileDescriptor.close()
    binary.close()


if __name__ == '__main__':
    print header

    arguments = argparse.ArgumentParser(
        description='Like ancient viking, searching for code cave in a PE file.\nAlright.'
    )

    arguments.add_argument(
        '-f',
        '--file',
        dest='file',
        action='store',
        required=True,
        help='Path of your PE file',
    )

    arguments.add_argument(
        '-m',
        '--min',
        dest='minimumCaveSize',
        action='store',
        required=False,
        default=450,              # Basic Metasploit payload
        help='Minimum size of your desired code cave',
    )

    arguments.add_argument(
        '-s',
        '--section',
        dest='targetedSection',
        action='store',
        required=False,
        help='The section where you want to search a code cave',
    )

    arguments = arguments.parse_args()

    if arguments.file:
        main(arguments.file, arguments.minimumCaveSize, arguments.targetedSection)
    else:
        arguments.print_help()
        sys.exit()
