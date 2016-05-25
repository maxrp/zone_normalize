import gzip
import sys

from . import zone_iterator, zone_dict_to_str, ZONE_FMT_STR

try:
    from colorama import Fore, init as colorama_init
except ImportError:
    HAS_COLOR = False
else:
    HAS_COLOR = True


def main():
    if HAS_COLOR:
        colors = [Fore.GREEN, Fore.MAGENTA, Fore.BLUE, Fore.CYAN, Fore.YELLOW]

        colorama_init(autoreset=True)
        unpacked_fmt = ZONE_FMT_STR.split()
        color_format = " ".join([color for segment in
                                 zip(colors, unpacked_fmt)
                                 for color in segment])

    zone_file = sys.argv[1]
    if zone_file[-2:] == 'gz':
        our_open = gzip.open
    else:
        our_open = open

    with our_open(zone_file, mode='rt') as zonefh:
        for record in zone_iterator(zonefh):
            print(zone_dict_to_str(record, fmt_str=color_format))

if __name__ == "__main__":
    main()
