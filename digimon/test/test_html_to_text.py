import unittest

from digimon.spiders import digimon_spider
from digimon import pipelines
from digimon.test.responses import fake_response_from_file

class HTMLToTextTest(unittest.TestCase):
    def setUp(self) -> None:
        self.spider = digimon_spider.DigimonSpider()

        
    def test_cenas(self):
        pass
        # pipeline = pipelines.HTMLToText()
        # pipeline.process_item({
        # })
