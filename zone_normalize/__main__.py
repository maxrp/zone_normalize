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

import argparse
import gzip

from pprint import PrettyPrinter

try:
    # colorama is an optional dep
    from colorama import Fore, init as colorama_init
except ImportError:
    HAS_COLOR = False
else:
    HAS_COLOR = True

from . import __version__, zone_normalize, zone_dict_to_str, ZONE_FMT_STR


def maybe_compressed_file(filename):
    if filename[-2:] == 'gz':
        our_open = gzip.open
    else:
        our_open = open

    return our_open(filename, mode='rt')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d',
                        '--dump',
                        action='store_true',
                        help='Dump a list of line structures instead of \
                        printing and coloring each entry.')
    parser.add_argument('-nc',
                        '--no-color',
                        action='store_true',
                        help='Disable color.')
    parser.add_argument('-v',
                        '--version',
                        action='store_true',
                        help='Display version information.')
    parser.add_argument('zones',
                        nargs='*',
                        type=maybe_compressed_file,
                        help='A file or list of zone files, optionally these \
                        files may be gzipped.')
    args = parser.parse_args()

    if args.version:
        print("zone-highlight (zone_normalize) {}".format(__version__))
        print("Copyright (C) 2016 Max R.D. Parmer")
        print("License AGPLv3+: GNU Affero GPL version 3 or later.")
        print("            <http://www.gnu.org/licenses/agpl.html>")

    if HAS_COLOR and not args.no_color:
        colors = [Fore.GREEN, Fore.MAGENTA, Fore.BLUE, Fore.CYAN, Fore.YELLOW]

        colorama_init(autoreset=True)
        unpacked_fmt = ZONE_FMT_STR.split()
        final_format = " ".join([color for segment in
                                 zip(colors, unpacked_fmt)
                                 for color in segment])
    else:
        final_format = ZONE_FMT_STR

    for zone in args.zones:
        with zone as zonefh:
            if args.dump:
                pp = PrettyPrinter(indent=4, compact=True, width=72)
                pp.pprint([l for l in zone_normalize(zonefh)])
            else:
                for record in zone_normalize(zonefh):
                    print(zone_dict_to_str(record, fmt_str=final_format))


if __name__ == "__main__":
    main()
