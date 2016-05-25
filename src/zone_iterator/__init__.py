from collections import OrderedDict
from typing import Any, Dict, Iterator, Iterable, List, Tuple

# should be exhaustive
RECORDCLASSES = ['ch', 'in', 'hs', 'cs']
# non-exhaustive
RECORDTYPES = ['a',
               'aaaa',
               'dnskey',
               'rrsig',
               'ns',
               'nsec',
               'nsec3',
               'nsec3param',
               'txt']
# Basic format for a zone and data
ZONE_FMT_STR = "{0[origin]} {0[ttl]} {0[class]} {0[type]} {1}"


def split_comments(line: str) -> Tuple[str, str]:
    semicolon = line.index(';')
    return (line[0:semicolon].strip(), line[semicolon+1:].strip())


def set_defaults(line: str, default_values: Dict[str, str]) -> Dict[str, str]:
    var_name, var_value = tuple(line[1:].split())
    var_name = var_name.lower()
    default_values[var_name] = var_value.lower()
    return default_values


def set_flags(line: str, multiline: bool) -> Tuple[bool, bool, bool]:
    comments = False
    end_of_multiline = False

    for token in line:
        if not multiline and token == '(':
            multiline = True
        if multiline and token == ')':
            end_of_multiline = True
        if token == ';':
            comments = True
    return (comments, multiline, end_of_multiline)


def zone_dict_to_str(record: OrderedDict, fmt_str: str=ZONE_FMT_STR) -> str:
    return fmt_str.format(record, " ".join(record['data']))


def zone_iterator(zone_file: Iterable, def_class="in", ttl="900") -> Iterator:
    default_values = {'class': def_class,
                      'ttl': ttl}
    multiline = False
    multiline_str = ''
    for line in zone_file:
        if line.startswith('$'):
            default_values = set_defaults(line, default_values)
            continue

        comments, multiline, end_of_multiline = set_flags(line, multiline)
        if comments:
            line, _ = split_comments(line)

        if multiline:
            multiline_str += "{} ".format(line)
            if not end_of_multiline:
                continue
            else:
                line = multiline_str
                multiline_str = ''
                multiline = False

        line_chunks = line.strip().split()
        line_len = len(line_chunks)

        # We need this line to at least be two fields, type and data
        if line_len < 2:
            continue

        # replace @ with origin
        if line_chunks[0] == '@':
            line_chunks[0] = default_values['origin']

        # always lowercase the first field
        line_chunks[0] = line_chunks[0].lower()

        # A two field [type, data] entry, needs three fields added
        if line_chunks[0] in RECORDTYPES and line_len == 2:
            line_chunks.insert(0, default_values['class'])
            line_chunks.insert(0, default_values['ttl'])
            line_chunks.insert(0, default_values['origin'])

        # Normalize case in the first three fields for ease of comparison
        for i in range(1, 3):
            line_chunks[i] = line_chunks[i].lower()

        if line_chunks[1] in RECORDCLASSES and line_chunks[2] in RECORDTYPES:
            # then the first field is the ttl
            line_chunks.insert(0, default_values['origin'])

        # if the first char of the first field isn't numeric and the second is
        # a class, inject a ttl field
        if line_chunks[1] in RECORDCLASSES \
                and not line_chunks[0][0].isnumeric():
            line_chunks.insert(1, default_values['ttl'])
        # if the second field is a known record type inject a ttl and class
        elif line_chunks[1] in RECORDTYPES:
            line_chunks.insert(1, default_values['class'])
            line_chunks.insert(1, default_values['ttl'])

        if not line_chunks[0].endswith('.'):
            line_chunks[0] += '.' + default_values['origin']

        # try to name the fields
        record = OrderedDict()  # type: OrderedDict[str, str]
        record['origin'], record['ttl'], record['class'], record['type'] = \
            tuple(line_chunks[:4])

        # the rest of the data goes here and needs a type specific parser
        record['data'] = line_chunks[4:]

        if 'origin' not in default_values:
            default_values['origin'] = record['origin']

        yield record
