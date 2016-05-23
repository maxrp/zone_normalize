import pytest

from collections import OrderedDict
from zone_iterator import split_comments, zone_iterator, zone_dict_to_str

REFERENCE_COM_ZONE = [OrderedDict([('origin', 'com.'),
                                   ('ttl', '900'),
                                   ('class', 'in'),
                                   ('type', 'soa'),
                                   ('data', ['a.gtld-servers.net.',
                                             'nstld.verisign-grs.com.', '(',
                                             '1463069743',
                                             '1800',
                                             '900',
                                             '604800',
                                             '86400', ')'])]),
                      OrderedDict([('origin', 'com.'),
                                   ('ttl', '172800'),
                                   ('class', 'in'),
                                   ('type', 'ns'),
                                   ('data', ['A.GTLD-SERVERS.NET.'])]),
                      OrderedDict([('origin', 'ns2.muscleextremexxl.com.'),
                                   ('ttl', '172800'),
                                   ('class', 'in'),
                                   ('type', 'a'),
                                   ('data', ['149.255.57.124'])]),
                      OrderedDict([('origin', 'ns3.muscleextremexxl.com.'),
                                   ('ttl', '172800'),
                                   ('class', 'in'),
                                   ('type', 'a'),
                                   ('data', ['193.105.134.6'])]),
                      OrderedDict([('origin', 'ns1.muscleextremexxl.com.'),
                                   ('ttl', '172800'),
                                   ('class', 'in'),
                                   ('type', 'a'),
                                   ('data', ['31.220.42.157'])]),
                      OrderedDict([('origin', 'ns1.newpointnet.com.'),
                                   ('ttl', '172800'),
                                   ('class', 'in'),
                                   ('type', 'a'),
                                   ('data', ['208.67.44.155'])]),
                      OrderedDict([('origin', 'ns2.newpointnet.com.'),
                                   ('ttl', '172800'),
                                   ('class', 'in'),
                                   ('type', 'a'),
                                   ('data', ['198.175.28.6'])]),
                      OrderedDict([('origin', 'ns0.world-of-digital.com.'),
                                   ('ttl', '172800'),
                                   ('class', 'in'),
                                   ('type', 'a'),
                                   ('data', ['212.227.82.151'])]),
                      OrderedDict([('origin', 'ns.hemendemo.com.'),
                                   ('ttl', '172800'),
                                   ('class', 'in'),
                                   ('type', 'a'),
                                   ('data', ['185.87.121.219'])]),
                      OrderedDict([('origin', 'www.poldega.com.'),
                                   ('ttl', '172800'),
                                   ('class', 'in'),
                                   ('type', 'a'),
                                   ('data', ['89.16.164.137'])]),
                      OrderedDict([('origin', 'vrsn-end-of-zone-marker-dummy-record.com.'),
                                   ('ttl', '172800'),
                                   ('class', 'in'),
                                   ('type', 'txt'),
                                   ('data', ['plenus'])])]


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
        implicit_origin_zone = [zone_dict_to_str(REFERENCE_COM_ZONE[0]),
                                zone_dict_to_str(REFERENCE_COM_ZONE[1])]
        zone = [l for l in zone_iterator(implicit_origin_zone)]
        assert REFERENCE_COM_ZONE[0:2] == zone
