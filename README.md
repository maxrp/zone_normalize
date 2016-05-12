# zone_iterator 

This package provides an iterator which on each iteration yields a normalized
zone entry.

This project stands in contrast to [dnspython][1] which requires physical
memory similar to the size of the input zone file. Unlike dnspython this can
operate in constant space. This is important for handling large, multi-gigabyte
zone files.

[1]: http://www.dnspython.org/
