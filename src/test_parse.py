import pytest

from collections import OrderedDict
from zone_iterator import split_comments, zone_iterator, zone_dict_to_str

REFERENCE_COM_ZONE = [OrderedDict([('origin', 'com.'),
                                   ('ttl', '900'),
                                   ('class', 'in'),
                                   ('type', 'soa'),
                                   ('data',
                                   ['a.gtld-servers.net.',
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
                                   ('data', ['a.gtld-servers.net.'])]),
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
                      OrderedDict([('origin',
                                    'vrsn-end-of-zone-marker-dummy-record.com.'
                                    ),
                                   ('ttl', '172800'),
                                   ('class', 'in'),
                                   ('type', 'txt'),
                                   ('data', ['plenus'])])]

RFC1035_EXAMPLE = [OrderedDict([('origin', 'isi.edu.'),
                                ('ttl', '900'),
                                ('class', 'in'),
                                ('type', 'soa'),
                                ('data',
                                ['venera', 'action\\.domains',
                                 '(', '20', '7200', '600', '3600000',
                                 '60)'])]),
                   OrderedDict([('origin', 'isi.edu.'),
                                ('ttl', '900'),
                                ('class', 'in'),
                                ('type', 'ns'),
                                ('data', ['a.isi.edu.'])]),
                   OrderedDict([('origin', 'isi.edu.'),
                                ('ttl', '900'),
                                ('class', 'in'),
                                ('type', 'ns'),
                                ('data', ['venera'])]),
                   OrderedDict([('origin', 'isi.edu.'),
                                ('ttl', '900'),
                                ('class', 'in'),
                                ('type', 'ns'),
                                ('data', ['vaxa'])]),
                   OrderedDict([('origin', 'isi.edu.'),
                                ('ttl', '900'),
                                ('class', 'in'),
                                ('type', 'mx'),
                                ('data', ['10', 'venera'])]),
                   OrderedDict([('origin', 'isi.edu.'),
                                ('ttl', '900'),
                                ('class', 'in'),
                                ('type', 'mx'),
                                ('data', ['20', 'vaxa'])]),
                   OrderedDict([('origin', 'isi.edu.'),
                                ('ttl', '900'),
                                ('class', 'in'),
                                ('type', 'a'),
                                ('data', ['a', '26.3.0.103'])]),
                   OrderedDict([('origin', 'venera.isi.edu.'),
                                ('ttl', '900'),
                                ('class', 'in'),
                                ('type', 'a'),
                                ('data', ['10.1.0.52'])]),
                   OrderedDict([('origin', 'isi.edu.'),
                                ('ttl', '900'),
                                ('class', 'in'),
                                ('type', 'a'),
                                ('data', ['128.9.0.32'])]),
                   OrderedDict([('origin', 'vaxa.isi.edu.'),
                                ('ttl', '900'),
                                ('class', 'in'),
                                ('type', 'a'),
                                ('data', ['10.2.0.27'])]),
                   OrderedDict([('origin', 'isi.edu.'),
                                ('ttl', '900'),
                                ('class', 'in'),
                                ('type', 'a'),
                                ('data', ['128.9.0.33'])])]

# the first 9 lines expected from parsing rfc4035.zone
RFC4035_EXAMPLE = [OrderedDict([('origin', 'example.'),
                                ('ttl', '3600'),
                                ('class', 'in'),
                                ('type', 'soa'),
                                ('data',
                                ['ns1.example.',
                                 'bugs.x.w.example.', '(',
                                 '1081539377', '3600', '300', '3600000',
                                 '3600', ')'])]),
                   OrderedDict([('origin', 'example.'),
                                ('ttl', '3600'),
                                ('class', 'in'),
                                ('type', 'rrsig'),
                                ('data',
                                ['soa', '5', '1', '3600',
                                 '20040509183619',
                                 '(', '20040409183619',
                                 '38519', 'example.',
                                 'onx0k36rcjaxytcngq6iqnpnv5+drqyasc9h',
                                 '7tsjahcqbhe67sr6ah2xdugcqqwu/n0uvzrf',
                                 'vkgo9ebarz0gwdkcuwlm6enb5six2k74l5lw',
                                 'da7s/un/ibtdq4ay8nmnlqi7dw7n4p8/rjkb',
                                 'jv7j86hyqgm5e7+miraz8v01b0i=',
                                 ')'])]),
                   OrderedDict([('origin', 'example.'),
                                ('ttl', '3600'),
                                ('class', 'in'),
                                ('type', 'ns'),
                                ('data', ['ns1.example.'])]),
                   OrderedDict([('origin', 'example.'),
                                ('ttl', '3600'),
                                ('class', 'in'),
                                ('type', 'ns'),
                                ('data', ['ns2.example.'])]),
                   OrderedDict([('origin', 'example.'),
                                ('ttl', '3600'),
                                ('class', 'in'),
                                ('type', 'rrsig'),
                                ('data',
                                ['ns', '5', '1', '3600',
                                 '20040509183619',
                                 '(', '20040409183619',
                                 '38519',
                                 'example.',
                                 'gl13f00f2u0r+swixxlhwsmy+qstyy5k6zfd',
                                 'euivwc+wd1fmbncyql0tk7lhtx6uoxc8agnf',
                                 '4isfve8xqf4q+o9qlnqizmppu3linekt4fz8',
                                 'ro5urfovomrtbqxw3u0hxwugge4g3zpshv48',
                                 '0hjmerazb/frpgfjpajngcq6kwg=',
                                 ')'])]),
                   OrderedDict([('origin', 'example.'),
                                ('ttl', '3600'),
                                ('class', 'in'),
                                ('type', 'mx'),
                                ('data', ['1', 'xx.example.'])]),
                   OrderedDict([('origin', 'example.'),
                                ('ttl', '3600'),
                                ('class', 'in'),
                                ('type', 'rrsig'),
                                ('data',
                                ['mx', '5', '1', '3600',
                                 '20040509183619',
                                 '(', '20040409183619',
                                 '38519',
                                 'example.',
                                 'hydhyvt5khsz7hto/vypumpmszqrcop3tzwb',
                                 '2qakkhvpfau/dglgs/ikenkyogl95g4n+nze',
                                 'vynu8dctockt+chpcgevjguq7a3ao9z/zkuo',
                                 '6gmmuw4b89rz1puxw4jzuxj66ptwovtuu/im',
                                 'w6oisukd1eqt7a0kygkg+pedxdi=',
                                 ')'])]),
                   OrderedDict([('origin', 'example.'),
                                ('ttl', '3600'),
                                ('class', 'in'),
                                ('type', 'nsec'),
                                ('data',
                                ['a.example.',
                                 'ns', 'soa', 'mx', 'rrsig',
                                 'nsec', 'dnskey'])]),
                   OrderedDict([('origin', 'example.'),
                                ('ttl', '3600'),
                                ('class', 'in'),
                                ('type', 'rrsig'),
                                ('data',
                                ['nsec', '5', '1', '3600',
                                 '20040509183619',
                                 '(', '20040409183619',
                                 '38519', 'example.',
                                 'o0k558jhhyrc97ishnislm4klmw48c7u7cbm',
                                 'ftfhke5ivqnrvtb1stlmpgpbdic9hcryoo0v',
                                 'z9me5xpzuehbvgnhd5sfzgfvegxr5nyyq4tw',
                                 'sdbgibilquv1ivy29vhxy7wgr62dprz0pwvm',
                                 'jffj5arxf4npxp/keowggbrzy/u=',
                                 ')'])])]

RFC5155_EXAMPLE = [OrderedDict([('origin', 'example.'),
                                ('ttl', '3600'),
                                ('class', 'in'),
                                ('type', 'soa'),
                                ('data',
                                ['ns1.example.', 'bugs.x.w.example.', '1',
                                 '3600', '300', '(', '3600000', '3600',
                                 ')'])]),
                   OrderedDict([('origin', 'example.'),
                                ('ttl', '3600'),
                                ('class', 'in'),
                                ('type', 'rrsig'),
                                ('data',
                                ['soa', '7', '1', '3600', '20150420235959',
                                 '20051021000000', '(', '40430', 'example.',
                                 'hu25uiynpmvpivbrldn+9mlp9zql39qaud8i',
                                 'q4zllywfuubbas41pg+68z81q1xhkyaceyhd',
                                 'vi2lmkusbzst0q==', ')'])]),
                   OrderedDict([('origin', 'example.'),
                                ('ttl', '3600'),
                                ('class', 'in'),
                                ('type', 'ns'),
                                ('data', ['ns1.example.'])]),
                   OrderedDict([('origin', 'example.'),
                                ('ttl', '3600'),
                                ('class', 'in'),
                                ('type', 'ns'),
                                ('data', ['ns2.example.'])]),
                   OrderedDict([('origin', 'example.'),
                                ('ttl', '3600'),
                                ('class', 'in'),
                                ('type', 'rrsig'),
                                ('data',
                                ['ns', '7', '1', '3600', '20150420235959',
                                 '20051021000000', '(', '40430', 'example.',
                                 'pvogtmk1hhestau+hwdwc8ts+6c8qtqd4pqj',
                                 'qotdevgg+ma+ai4fwdehu3qhjylcq9tbd2vv',
                                 'cnmxjtz6syobxa==', ')'])]),
                   OrderedDict([('origin', 'example.'),
                                ('ttl', '3600'),
                                ('class', 'in'),
                                ('type', 'mx'),
                                ('data', ['1', 'xx.example.'])]),
                   OrderedDict([('origin', 'example.'),
                                ('ttl', '3600'),
                                ('class', 'in'),
                                ('type', 'rrsig'),
                                ('data',
                                ['mx', '7', '1', '3600', '20150420235959',
                                 '20051021000000', '(', '40430', 'example.',
                                 'ggq1a9xs47k42vpvpl/a1bwuz/6xsnhkjotw',
                                 '9so8mqtztl2wjbsnoqsaohrrcrrbyriel/gz',
                                 'n9mto/kx+wbo+w==', ')'])]),
                   OrderedDict([('origin', 'example.'),
                                ('ttl', '3600'),
                                ('class', 'in'),
                                ('type', 'dnskey'),
                                ('data',
                                ['256', '3', '7',
                                 'aweaaaetidlzskwut4swwr8yu0wphpiui8lu', '(',
                                 'sad0qpwu+wzt89epo6thzkmbvdkc7qphqo2h',
                                 'ty4hhn9npwfrw5byube=', ')'])]),
                   OrderedDict([('origin', 'example.'),
                                ('ttl', '3600'),
                                ('class', 'in'),
                                ('type', 'dnskey'),
                                ('data',
                                ['257', '3', '7',
                                 'aweaaculfv1vhmqx6nsouoq2r/dsr7xm3upj', '(',
                                 'j7iommwspjabvfw8q0rovxdm6kzt+tau92l9',
                                 'absudblmfin8cvf3n4s=', ')'])])]


@pytest.fixture()
def sample_com_tld():
    com_zone = open('tests/data/com.zone', mode='rt')

    def fin():
        com_zone.close()

    return com_zone


@pytest.fixture()
def rfc_examples():
    rfcs = [1035, 4035, 5155]
    zones = {}

    for rfc in rfcs:
        zones[rfc] = open('tests/data/rfc{}.zone'.format(rfc), mode='rt')

    def fin():
        for rfc in rfcs:
            zones[rfc].close()

    return zones


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

    @pytest.mark.usefixtures("rfc_examples")
    def test_rfc_examples(self, rfc_examples):
        zone1035 = [l for l in zone_iterator(rfc_examples[1035])]
        zone4035 = [l for l in zone_iterator(rfc_examples[4035])]
        zone5155 = [l for l in zone_iterator(rfc_examples[5155])]
        assert RFC1035_EXAMPLE == zone1035
        assert RFC4035_EXAMPLE == zone4035[0:9]
        assert RFC5155_EXAMPLE == zone5155[0:9]
