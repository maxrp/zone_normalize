# This file is a part of zone_normalize: A package to parse, normalize
# and show DNS zone data
#
# Copyright (C) 2016 Max R.D. Parmer
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from collections import OrderedDict
from typing import Any, Dict, Iterator, Iterable, List, Tuple  # noqa

# semver
__version__ = "0.9.1.dev"

# should be exhaustive
RECORDCLASSES = ['ch', 'in', 'hs', 'cs']
# non-exhaustive, but fairly close
RECORDTYPES = ['a',
               'aaaa',
               'afsdb',
               'apl',
               'caa',
               'cdnskey',
               'cds',
               'cert',
               'cname',
               'dhcid',
               'dlv',
               'dname',
               'dnskey',
               'ds',
               'hinfo',
               'hip',
               'ipseckey',
               'key',
               'kx',
               'loc',
               'mx',
               'naptr',
               'ns',
               'nsec',
               'nsec3',
               'nsec3param',
               'ptr',
               'rp',
               'rrsig',
               'sig',
               'soa',
               'srv',
               'sshfp',
               'ta',
               'tkey',
               'tlsa',
               'tsig',
               'txt',
               'uri']
# Basic format for a zone and data
ZONE_FMT_STR = "{0[origin]} {0[ttl]} {0[class]} {0[type]} {1}"


def normalize_data(line: str, default_values: Dict[str, str]) -> List[str]:
    line_chunks = line.split()

    # replace @ with origin
    if line_chunks[0] == '@':
        line_chunks[0] = default_values['origin']

    # A two field [type, data] entry, needs three fields added
    if line_chunks[0] in RECORDTYPES:
        line_chunks.insert(0, default_values['class'])
        line_chunks.insert(0, default_values['ttl'])
        line_chunks.insert(0, default_values['origin'])
    # probably a three field record begining with TTL
    elif line_chunks[0].isnumeric() and not line_chunks[0].endswith('.'):
        line_chunks.insert(0, default_values['origin'])

    if not line_chunks[0].endswith('.'):
        line_chunks[0] += '.' + default_values['origin']

    # if the first char of the first field isn't numeric and the second is
    # a class, inject a ttl field
    if line_chunks[1] in RECORDCLASSES \
            and not line_chunks[0][0].isnumeric():
        line_chunks.insert(1, default_values['ttl'])
    # if the second field is a known record type inject a ttl and class
    elif line_chunks[1] in RECORDTYPES:
        line_chunks.insert(1, default_values['class'])
        line_chunks.insert(1, default_values['ttl'])

    if line_chunks[1].isnumeric() and line_chunks[2] in RECORDTYPES:
        line_chunks.insert(2, default_values['class'])

    return line_chunks


def split_comments(line: str) -> Tuple[str, str]:
    semicolon = line.index(';')
    return (line[0:semicolon].strip(), line[semicolon+1:].strip())


def set_defaults(line: str, default_values: Dict[str, str]) -> Dict[str, str]:
    var_name, var_value = tuple(line[1:].split())
    var_name = var_name
    default_values[var_name] = var_value
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


def zone_normalize(zone_file: Iterable, def_class="in", ttl="900") -> Iterator:
    default_values = {'class': def_class,
                      'ttl': ttl}
    multiline = False
    multiline_str = ''
    for line in zone_file:
        line = line.strip().lower()
        record = OrderedDict()  # type: OrderedDict[str, Any]

        if line.startswith('$'):
            default_values = set_defaults(line, default_values)
            continue

        comments, multiline, end_of_multiline = set_flags(line, multiline)
        if comments:
            line, _ = split_comments(line)

        if line:
            if multiline:
                multiline_str += "{} ".format(line)
                if not end_of_multiline:
                    continue
                else:
                    line = multiline_str
                    multiline_str = ''
                    multiline = False

            line_chunks = normalize_data(line, default_values)

            # try to name the fields
            record['origin'], record['ttl'], record['class'], record['type'] \
                = tuple(line_chunks[:4])
            # the rest of the data goes here and needs a type specific parser
            record['data'] = line_chunks[4:]

            if 'origin' not in default_values:
                default_values['origin'] = record['origin']
            default_values['ttl'] = record['ttl']

            yield record
