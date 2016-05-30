# zone_normalize and zone-highlight
## A package to parse and normalize DNS zone data (and a CLI zone highlighter)

This package (zone_normalize) provides an iterator which on each iteration
yields a normalized zone entry, based on this library the utility
`zone-highlight` is provided which prints a highlighted and normalized zone.

This project stands in contrast to [dnspython][1] which requires physical
memory similar to the size of the input zone file. Unlike dnspython this can
operate in constant space. This is important for handling large, multi-gigabyte
zone files.

[1]: http://www.dnspython.org/
