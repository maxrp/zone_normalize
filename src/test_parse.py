from zone_iterator import *

class TestParse:
    def test_comment_split(self):
        simple_test_comment = "; foobar"
        assert split_comments(simple_test_comment) == \
                ('', 'foobar')
