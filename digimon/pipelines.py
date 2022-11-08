from itemadapter import ItemAdapter
import re
from scrapy.exceptions import DropItem

class DigimonPipeline:
    def process_item(self, item, spider):
        return item


class HTMLToText:
    def process_item(self, item, spider):
        url = item['url']

        if item['name'] in [None, '']:
            raise DropItem(f'Missing name in: {url}')

        return item
