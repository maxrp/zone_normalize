from typing import Dict, Iterator, Iterable, List, Tuple

import sys

# should be exhaustive
RECORDCLASSES = ['ch', 'in', 'hs', 'cs']
# non-exhaustive
RECORDTYPES = ['a', 'aaaa', 'ns', 'rrsig', 'nsec', 'nsec3', 'nsec3param', 'dnskey', 'txt']

def split_comments(line: str) -> Tuple[str, str]:
    semicolon = line.index(';')
    return (line[0:semicolon].strip(), line[semicolon+1:].strip())


def set_defaults(line: str, default_values: Dict[str, str]) -> Dict[str, str]:
    var_name, var_value = tuple(line[1:].split())
    var_name = var_name.lower()
    default_values[var_name] = var_value
    return default_values


def set_flags(line: str, multiline: bool) -> Tuple[bool, bool]:
    comments = False

    for token in line:
        if not multiline and token == '(':
            multiline = True
        if token == ';':
            comments = True
    return (comments, multiline)


def zone_iterator(zone_file: Iterable,
                  default_class="in",
                  default_ttl="900") -> Iterator[List[str]]:
    default_values = {'class': default_class,
                      'ttl': default_ttl}
    multiline = False
    multiline_str = ''
    for line in zone_file:
        if line.startswith('$'):
            default_values = set_defaults(line, default_values)
            continue

        comments, multiline = set_flags(line, multiline)
        if comments:
            line, _ = split_comments(line)

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

        # replace @ with origin
        if line_chunks[0] == '@':
            line_chunks[0] = default_values['origin']

        # Fixing phase
        if line_chunks[1].lower() in RECORDCLASSES:
            line_chunks.insert(1, default_values['ttl'])
        elif line_chunks[1].lower() in RECORDTYPES:
            # is the second field a known record type? then inject a TTL
            line_chunks.insert(1, default_values['class'])
            line_chunks.insert(1, default_values['ttl'])
        elif line_chunks[0].lower() in RECORDTYPES:
            line_chunks.insert(0, default_values['class'])
            line_chunks.insert(0, default_values['ttl'])
            line_chunks.insert(0, default_values['origin'])

        if not line_chunks[0].endswith('.'):
            line_chunks[0] += '.' + default_values['origin']

        yield line_chunks
