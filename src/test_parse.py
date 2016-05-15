import pytest

from zone_iterator import *

REFERENCE_COM_ZONE = [['COM.',
                       'IN',
                       'SOA',
                       'a.gtld-servers.net.',
                       'nstld.verisign-grs.com.',
                       '(',
                       '1463069743',
                       '1800',
                       '900',
                       '604800',
                       '86400',
                       ')'],
                      ['COM.', '172800', 'NS', 'A.GTLD-SERVERS.NET.'],
                      ['NS2.MUSCLEEXTREMEXXL.COM.', '172800', 'A', '149.255.57.124'],
                      ['NS3.MUSCLEEXTREMEXXL.COM.', '172800', 'A', '193.105.134.6'],
                      ['NS1.MUSCLEEXTREMEXXL.COM.', '172800', 'A', '31.220.42.157'],
                      ['NS1.NEWPOINTNET.COM.', '172800', 'A', '208.67.44.155'],
                      ['NS2.NEWPOINTNET.COM.', '172800', 'A', '198.175.28.6'],
                      ['NS0.WORLD-OF-DIGITAL.COM.', '172800', 'A', '212.227.82.151'],
                      ['NS.HEMENDEMO.COM.', '172800', 'A', '185.87.121.219'],
                      ['WWW.POLDEGA.COM.', '172800', 'A', '89.16.164.137'],
                      ['VRSN-END-OF-ZONE-MARKER-DUMMY-RECORD.com.', 'TXT', 'plenus']]

@pytest.fixture()
def sample_com_tld():
    com_zone = open('tests/data/com.zone', mode='rt')
    def fin():
        com_zone.close()
    return com_zone

@pytest.mark.usefixtures("sample_com_tld")
class TestParse:
    def test_comment_split(self):
        simple_test_comment = "; foobar"
        _, comment = split_comments(simple_test_comment)
        assert comment == "foobar"

    def test_rdata_split(self):
        test_comment = "example.com. NS ns1.example.com ; an example NS record"
        rdata, _ = split_comments(test_comment)
        assert rdata == "example.com. NS ns1.example.com"

    def test_com_tld_parse(self, sample_com_tld):
        zone = [l for l in zone_iterator(sample_com_tld)]
        assert zone == REFERENCE_COM_ZONE
