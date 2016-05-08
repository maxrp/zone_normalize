#!/usr/bin/python

import gzip
import sys

from collections import defaultdict

def strip_comments(line):
    semicolon = line.index(';')
    return line[0:semicolon].strip()

def parse_zone(zone_file):
    dispatch = defaultdict(None, {})
    with gzip.open(zone_file, mode='rt') as zonefh:
        multiline = False
        multiline_str = ''
        for line in zonefh:
            if ';' in line:
                line = strip_comments(line)

            if '(' in line:
                multiline = True

            if multiline:
                multiline_str += "{} ".format(line)
                if ')' in multiline_str:
                    line = multiline_str
                    multiline = False
                else:
                    continue
          
            line = line.strip().split()
            if line:
                yield line

def main():
    zone_file = sys.argv[1]
    for line in parse_zone(zone_file):
        print(line)

if __name__ == '__main__':
    main()
