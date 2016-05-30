# zone_normalize and zone-highlight
**A package to parse and normalize DNS zone data (and a CLI zone highlighter)**

Zone_normalize) provides an iterator which on each iteration yields a
normalized DNS zone entry, based on this library the utility `zone-highlight`
is provided which prints a highlighted and normalized zone.

This project stands in contrast to [dnspython][1] which requires physical
memory similar to the size of the input zone file. Unlike dnspython this can
operate in constant space. This is important for handling large, multi-gigabyte
zone files.

[1]: http://www.dnspython.org/

### Standards Compliance
I've made an informal effort to adhere to RFCs 1035[2] and 4343[3] and have
included example zones from RFCs 4035[4] and 5155[5] as a part of the test
suite. In addition to RFC based test vectors, I've included excerpts of the TLD
zone files for .org, .net, .name, .fail and .com -- at this time only .com is
used in the test suite.

[2]: https://tools.ietf.org/html/rfc1035
[3]: https://tools.ietf.org/html/rfc4343
[4]: https://tools.ietf.org/html/rfc4035
[5]: https://tools.ietf.org/html/rfc5155
