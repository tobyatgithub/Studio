"""
Test East Cree G2P
"""

import os
import io
from unittest import main, TestCase
from lxml import etree

from readalongs.log import LOGGER
from readalongs.g2p.tokenize_xml import tokenize_xml
from readalongs.g2p.add_ids_to_xml import add_ids
from readalongs.g2p.convert_xml import convert_xml

class TestSouthEastCreeG2P(TestCase):
    def setUp(self):
        self.EXPECTED_TOKENIZED = io.open(
            os.path.join(os.path.dirname(__file__),
                        'test_crj_sample_tokenized.xml')).read().strip()
        self.EXPECTED_IDS = io.open(os.path.join(os.path.dirname(__file__),
                                            'test_crj_sample_ids.xml')).read().strip()
        self.EXPECTED_CONVERTED = io.open(
            os.path.join(os.path.dirname(__file__),
                        'test_crj_sample_converted.xml')).read().strip()
        self.xml = etree.parse(os.path.join(os.path.dirname(__file__),
                                    'test_crj_sample.xml')).getroot()
        maxDiff = None

    def testTokenize(self):
        xml = tokenize_xml(self.xml)
        self.assertEqual(etree.tounicode(xml), self.EXPECTED_TOKENIZED)

    def testAddIDs(self):
        xml = tokenize_xml(self.xml)
        xml = add_ids(xml)
        self.assertEqual(etree.tounicode(xml), self.EXPECTED_IDS)

    def testConvert(self):
        xml = tokenize_xml(self.xml)
        xml = add_ids(xml)
        xml = convert_xml(xml)
        self.assertEqual(etree.tounicode(xml), self.EXPECTED_CONVERTED)

if __name__ == '__main__':
    LOGGER.setLevel('DEBUG')
    main()
