import pytest

from zone_iterator import split_comments, zone_iterator

REFERENCE_COM_ZONE = [['com.', '900', 'in', 'soa', 'a.gtld-servers.net.',
                       'nstld.verisign-grs.com.', '(',
                       '1463069743', '1800', '900', '604800', '86400', ')'],
                      ['com.', '172800', 'in', 'ns', 'A.GTLD-SERVERS.NET.'],
                      ['ns2.muscleextremexxl.com.', '172800', 'in', 'a',
                          '149.255.57.124'],
                      ['ns3.muscleextremexxl.com.', '172800', 'in', 'a',
                          '193.105.134.6'],
                      ['ns1.muscleextremexxl.com.', '172800', 'in', 'a',
                          '31.220.42.157'],
                      ['ns1.newpointnet.com.', '172800', 'in', 'a',
                          '208.67.44.155'],
                      ['ns2.newpointnet.com.', '172800', 'in', 'a',
                          '198.175.28.6'],
                      ['ns0.world-of-digital.com.', '172800', 'in', 'a',
                          '212.227.82.151'],
                      ['ns.hemendemo.com.', '172800', 'in', 'a',
                          '185.87.121.219'],
                      ['www.poldega.com.', '172800', 'in', 'a',
                          '89.16.164.137'],
                      ['vrsn-end-of-zone-marker-dummy-record.com.', '172800',
                          'in', 'txt', 'plenus']]


@pytest.fixture()
def sample_com_tld():
    com_zone = open('tests/data/com.zone', mode='rt')

    def fin():
        com_zone.close()

    return com_zone


class TestParse:
    def test_comment_split(self):
        simple_test_comment = "; foobar"
        _, comment = split_comments(simple_test_comment)
        assert "foobar" == comment

    def test_rdata_split(self):
        test_comment = "example.com. NS ns1.example.com ; an example NS record"
        rdata, _ = split_comments(test_comment)
        assert "example.com. NS ns1.example.com" == rdata

    @pytest.mark.usefixtures("sample_com_tld")
    def test_com_tld_parse(self, sample_com_tld):
        zone = [l for l in zone_iterator(sample_com_tld)]
        assert REFERENCE_COM_ZONE == zone

    def test_implicit_origin(self):
        implicit_origin_zone = [" ".join(REFERENCE_COM_ZONE[0]),
                                " ".join(REFERENCE_COM_ZONE[1][1:])]
        zone = [l for l in zone_iterator(implicit_origin_zone)]
        assert REFERENCE_COM_ZONE[0:2] == zone
