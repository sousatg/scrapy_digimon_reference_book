import unittest

from digimon.spiders import digimon_spider
from digimon.test.responses import fake_response_from_file

class DigimonSpiderTest(unittest.TestCase):
    def setUp(self) -> None:
        self.spider = digimon_spider.DigimonSpider()

    def _test_item_results(self, results, expected_length=0):
        result = list(results)
        self.assertEqual(result[0]['name'], 'Beelzemon')

    def test_parse_digimon(self):
        results = self.spider.parse_digimon_page(fake_response_from_file('digimon/Beelzemon.html', 'https://digimon.fandom.com/wiki/Beelzemon'))
        self._test_item_results(results)