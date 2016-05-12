import sys
from . import zone_iterator

def main():
    zone_file = sys.argv[1]
    for line in zone_iterator(zone_file):
        print(line)

if __name__ == "__main__":
    main()
