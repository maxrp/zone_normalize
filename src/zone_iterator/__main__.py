import gzip
import sys

from . import zone_iterator, zone_dict_to_str


def main():
    zone_file = sys.argv[1]
    if zone_file[-2:] == 'gz':
        our_open = gzip.open
    else:
        our_open = open

    with our_open(zone_file, mode='rt') as zonefh:
        for record in zone_iterator(zonefh):
            print(zone_dict_to_str(record))

if __name__ == "__main__":
    main()
