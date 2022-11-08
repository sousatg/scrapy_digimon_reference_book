from itemadapter import ItemAdapter
import html2text
import re
from scrapy.exceptions import DropItem


h = html2text.HTML2Text()
h.ignore_links = True
h.ignore_emphasis = True

class DigimonPipeline:
    def process_item(self, item, spider):
        return item


class HTMLToText:
    def _extract_table_data(self, html, join=False):       
        if html is None:
            return ''

        if isinstance(html, list):
            return html

        html = html.strip()

        text = h.handle(html)

        text = re.sub(r'##', '', text)
        text = re.sub('\\\\', '', text)
        text = re.sub('• ', '', text)

        lines = text.split('\n')

        lines = [re.sub(r'\[\d*\]', '', el.strip()) for el in lines if len(el.strip()) > 0]

        if join:
            lines = ' '.join(lines)

        return lines

    def _handle_original_name(self, value):
        original_name = ' '.join(value)

        original_name = re.sub(r'\(\s', '(', original_name)
        original_name = re.sub(r'\s\)', ')', original_name)
        original_name = re.sub(r'\s\s+', ' ', original_name)

        return original_name

    def process_item(self, item, spider):
        url = item['url']

        if item['name'] in [None, '']:
            raise DropItem(f'Missing name in: {url}')

        for key in item.keys():
            value = item[key]

            if key not in ['original_name', 'url', 'name', 'image']:
                value = self._extract_table_data(value)

            if key == 'original_name':
                value = self._handle_original_name(value)

            item[key] = value

        return item
