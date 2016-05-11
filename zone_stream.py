#!/usr/bin/python

import gzip
import sys

RECORDTYPES = ['a', 'aaaa', 'ns', 'rrsig', 'nsec', 'nsec3', 'nsec3param', 'dnskey']

def split_comments(line):
    semicolon = line.index(';')
    return (line[0:semicolon].strip(), line[semicolon:].strip())

def parse_zone(zone_file):
    default_values = {}
    multiline = False
    multiline_str = ''
    with gzip.open(zone_file, mode='rt') as zonefh:
        for line in zonefh:
            if ';' in line:
                line, _ = split_comments(line)
            if '(' in line:
                multiline = True

            if multiline:
                multiline_str += "{} ".format(line)
                if ')' in multiline_str:
                    line = multiline_str
                    multiline = False
                    multiline_str = ''
                else:
                    continue

            line = line.strip().split()
            line_len = len(line)

            # midpoint filtering
            if line_len < 2:
                continue

            # set a new default value
            if line_len == 2 and line[0].startswith('$'):
                default_values[line[0][1:].lower()] = line[1]
                continue

            # replace @ with origin
            if line[0] == '@':
                line[0] = default_values['origin']

            # Fixing phase
            if line[1].lower() in RECORDTYPES:
                # is the second field a known record type? then inject a TTL
                line.insert(1, default_values['ttl'])
            elif line[0].lower() in RECORDTYPES:
                line.insert(0, default_values['ttl'])
                line.insert(0, default_values['origin'])

            if not line[0].endswith('.'):
                line[0] += '.' + default_values['origin']

            yield line

def main():
    zone_file = sys.argv[1]
    for line in parse_zone(zone_file):
        print(line)

if __name__ == '__main__':
    main()
