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
    # //div[@class = "pi-item"] | //section[@class = "pi-item"]/table
    # response.xpath(//div[h3/text() = 'Partners']/div//*).extract()

    def parse_digimon_page(self, response):
        data = {}

        data["name"] = response.xpath('//aside/h2/span[1]/text()').get()
        data["original_name"] = response.xpath('//aside/h2//text()').getall()
        data["image"] = response.xpath('//aside//figure/a/img/@src').get()
        data["url"] = response.request.url

        elements = response.xpath("//aside/div | //aside/section/table")
        for el in elements:
            key = el.xpath('./*[1]//text()').get()
            value = el.xpath('./*[2]').get()

            if key is not None:
                data[key] = value

        yield data

    def handle_errors(self):
        print("CENAS--------------------------------------------------------------------")