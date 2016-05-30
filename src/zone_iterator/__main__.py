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

from . import zone_iterator, zone_dict_to_str, ZONE_FMT_STR


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
    parser.add_argument('zones',
                        nargs='*',
                        type=maybe_compressed_file,
                        help='A file or list of zone files, optionally these \
                        files may be gzipped.')
    args = parser.parse_args()

    if HAS_COLOR:
        colors = [Fore.GREEN, Fore.MAGENTA, Fore.BLUE, Fore.CYAN, Fore.YELLOW]

        colorama_init(autoreset=True)
        unpacked_fmt = ZONE_FMT_STR.split()
        color_format = " ".join([color for segment in
                                 zip(colors, unpacked_fmt)
                                 for color in segment])

    for zone in args.zones:
        with zone as zonefh:
            if args.dump:
                pp = PrettyPrinter(indent=4, compact=True, width=72)
                pp.pprint([l for l in zone_iterator(zonefh)][0:9])
            else:
                for record in zone_iterator(zonefh):
                    print(zone_dict_to_str(record, fmt_str=color_format))


if __name__ == "__main__":
    main()
