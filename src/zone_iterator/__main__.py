import argparse
import gzip
import sys

from . import zone_iterator, zone_dict_to_str, ZONE_FMT_STR

try:
    from colorama import Fore, init as colorama_init
except ImportError:
    HAS_COLOR = False
else:
    HAS_COLOR = True


def maybe_compressed_file(filename):
    if filename[-2:] == 'gz':
        our_open = gzip.open
    else:
        our_open = open

    return our_open(filename, mode='rt')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('inputs', nargs='*', type=maybe_compressed_file)
    args = parser.parse_args()

    if HAS_COLOR:
        colors = [Fore.GREEN, Fore.MAGENTA, Fore.BLUE, Fore.CYAN, Fore.YELLOW]

        colorama_init(autoreset=True)
        unpacked_fmt = ZONE_FMT_STR.split()
        color_format = " ".join([color for segment in
                                 zip(colors, unpacked_fmt)
                                 for color in segment])

    for inputfile in args.inputs:
        with inputfile as zonefh:
            for record in zone_iterator(zonefh):
                print(zone_dict_to_str(record, fmt_str=color_format))


if __name__ == "__main__":
    main()
