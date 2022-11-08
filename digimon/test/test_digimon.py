import unittest

from digimon.spiders import digimon_spider
from digimon.test.responses import fake_response_from_file

class DigimonSpiderTest(unittest.TestCase):
    def setUp(self) -> None:
        self.spider = digimon_spider.DigimonSpider()

    def _test_item_results(self, results, expected_length=0):
        result = next(results)
        self.assertIsNotNone(result['name'])
        self.assertIsNotNone(result['url'])
        self.assertEqual(len(result), expected_length)

    def test_parse_digimon(self):
        results = self.spider.parse_digimon_page(fake_response_from_file('digimon/Beelzemon.html', 'https://digimon.fandom.com/wiki/Beelzemon'))
        self._test_item_results(results, 18)

    def test_parse_page_with_image_in_name(self):
        results = self.spider.parse_digimon_page(fake_response_from_file('digimon/Dodomon.html', 'https://digimon.fandom.com/wiki/Dodomon'))
        self._test_item_results(results, 9)

    def test_parse(self):
        url = 'https://digimon.fandom.com/wiki/Digimon_Reference_Book'
        file_path = 'digimon/Digimon_Reference_Book.html'
        results = list(self.spider.parse(fake_response_from_file(file_path, url)))

        self.assertEqual(len(results), 1490)

        for el in results:
            self.assertIsNotNone(el.url)
            