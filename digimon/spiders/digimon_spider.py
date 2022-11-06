import scrapy
import re
import html2text

h = html2text.HTML2Text()
h.ignore_links = True
h.ignore_emphasis = True

class DigimonSpider(scrapy.Spider):
    name = 'digimon'

    custom_settings = {'FEED_EXPORT_ENCODING': 'utf-8'}

    def start_requests(self):
        urls = ['https://digimon.fandom.com/wiki/Digimon_Reference_Book']

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response, **kwargs):
        p = re.compile(r'^\/wiki\/.*mon$')
        urls = response.xpath("//div[@class='wikia-gallery-item']/div[@class='lightbox-caption']/a/@href").getall()
        for url in urls:
            if not p.match(url):
                next
            yield scrapy.Request(f'https://digimon.fandom.com/{url}', callback=self.parse_digimon_page, errback=self.handle_errors)


    # //div[h3/a/text() = "Prior forms"]/div/a/text() | //div[h3/a/text() = "Prior forms"]/div/sup
    # //div[h3/text() = 'Partners']/div//*[not(preceding-sibling::br)]
    # //div[h3/text() = 'Partners']/div//*[following::br)]
    # // following :: td[@class='KKKK'] /

    # response.xpath(//div[h3/text() = 'Partners']/div//*).extract()

    def _extract_table_data(self, el, join=False):
        html = el.get()
        
        if html is None:
            return ''

        html = html.strip()

        text = h.handle(html)

        text = re.sub(r'##', '', text)
        text = re.sub('\\\\', '', text)
        text = re.sub('• ', '', text)

        lines = text.split('\n')

        # Remove references and filter empty items from the list
        lines = [re.sub(r'\[\d*\]', '', el.strip()) for el in lines if len(el.strip()) > 0]

        if join:
            lines = ' '.join(lines)

        return lines

    def parse_digimon_page(self, response):
        name = response.xpath('//aside/h2/span[1]/text()').get()

        original_name = ' '.join(response.xpath('//aside/h2//text()').getall())
        original_name = re.sub(r'\(\s', '(', original_name)
        original_name = re.sub(r'\s\)', ')', original_name)
        original_name = re.sub(r'\s\s+', ' ', original_name)

        image = response.xpath('//aside//figure/a/img/@src').get()
        title = self._extract_table_data(response.xpath('//div[h3/text() = "Title"]/div'))
        level = self._extract_table_data(response.xpath('//div[h3/a/text() = "Level"]/div'))
        digimon_type = self._extract_table_data(response.xpath('//div[h3/a/text() = "Type"]/div'))
        attribute = self._extract_table_data(response.xpath('//div[h3/a/text() = "Attribute"]/div'))
        family = self._extract_table_data(response.xpath('//div[h3/a/text() = "Family"]/div'))
        debut = self._extract_table_data(response.xpath('//div[h3/text() = "Debut"]/div'))
        prior_forms = self._extract_table_data(response.xpath('//div[h3/a/text() = "Prior forms"]/div'))
        next_forms = self._extract_table_data(response.xpath('//div[h3/a/text() = "Next forms"]/div'))
        slide_forms = self._extract_table_data(response.xpath('//div[h3/a/text() = "DigiFuse forms"]/div'))
        digi_fuse_forms = self._extract_table_data(response.xpath('//div[h3/a/text() = "DigiFuse forms"]/div'))
        partners = self._extract_table_data(response.xpath('//div[h3/text() = "Partners"]/div'))
        voice_actors = self._extract_table_data(response.xpath('//div[h3/text() = "Voice actors"]/div'))
        cards = self._extract_table_data(response.xpath('//div[h3/text() = "Cards"]/div'))
        other_name = self._extract_table_data(response.xpath('//table[caption/text() = "Other Names"]/tbody'))
        groups = self._extract_table_data(response.xpath('//table[caption/text() = "Groups"]/tbody'))
        variations = self._extract_table_data(response.xpath('//table[caption/text() = "Variations"]/tbody'))

        yield {
            "url": response.request.url,
            "name": name,
            "original_name": original_name,
            "image": image,
            "title": title,
            "level": level,
            "digimon_type": digimon_type,
            "attribute": attribute,
            "family": family,
            "debut": debut,
            "prior_forms": prior_forms,
            "next_forms": next_forms,
            "slide_forms": slide_forms,
            "digi_fuse_forms": digi_fuse_forms,
            "partners": partners,
            "voice_actors": voice_actors,
            "cards": cards,
            "other_name": other_name,
            "groups": groups,
            "variations": variations
        }

    def handle_errors(self):
        print("CENAS--------------------------------------------------------------------")