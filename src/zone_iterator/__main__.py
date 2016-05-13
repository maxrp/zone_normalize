import gzip
import sys

from . import zone_iterator

def main():
    zone_file = sys.argv[1]
    if zone_file[-2:] == 'gz':
        our_open = gzip.open
    else:
        our_open = open

    with our_open(zone_file, mode='rt') as zonefh:
        for line in zone_iterator(zonefh):
            print(' '.join(line))

if __name__ == "__main__":
    main()
