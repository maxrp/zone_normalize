from typing import Dict, Iterator, Iterable, List, Tuple

import sys

RECORDTYPES = ['a', 'aaaa', 'ns', 'rrsig', 'nsec', 'nsec3', 'nsec3param', 'dnskey']

def split_comments(line: str) -> Tuple[str, str]:
    semicolon = line.index(';')
    return (line[0:semicolon].strip(), line[semicolon+1:].strip())

def zone_iterator(zone_file: Iterable) -> Iterator[List[str]]:
    default_values = {} # type: Dict[str, str]
    multiline = False
    multiline_str = ''
    for line in zone_file:
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

        line_chunks = line.strip().split()
        line_len = len(line_chunks)

        # midpoint filtering
        if line_len < 2:
            continue

        # set a new default value
        if line_len == 2 and line_chunks[0].startswith('$'):
            default_values[line_chunks[0][1:].lower()] = line_chunks[1]
            continue

        # replace @ with origin
        if line_chunks[0] == '@':
            line_chunks[0] = default_values['origin']

        # Fixing phase
        if line_chunks[1].lower() in RECORDTYPES:
            # is the second field a known record type? then inject a TTL
            line_chunks.insert(1, default_values['ttl'])
        elif line_chunks[0].lower() in RECORDTYPES:
            line_chunks.insert(0, default_values['ttl'])
            line_chunks.insert(0, default_values['origin'])

        if not line_chunks[0].endswith('.'):
            line_chunks[0] += '.' + default_values['origin']

        yield line_chunks
