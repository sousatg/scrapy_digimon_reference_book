import scrapy
import re
from scrapy.loader import ItemLoader
from digimon.items import DigimonItem


XPATH_NAME = '//aside/h2/span[1]/text() | //aside/h2/text()[1]'
XPATH_ORIGINAL_NAME = '//aside/h2//text()'
XPATH_IMAGE = '//aside//figure/a/img/@src'
XPATH_TITLE = '//div[h3/text() = "Title"]/div'
XPATH_LEVEL = '//div[h3/a/text() = "Level"]/div'
XPATH_SIZE = '//div[h3/text() = "Size"]/div'
XPATH_DIGIMON_TYPE = '//div[h3/a/text() = "Type"]/div'
XPATH_ATTRIBUTES = '//div[h3/a/text() = "Attribute"]/div'
XPATH_FAMILY = '//div[h3/a/text() = "Family"]/div'
XPATH_DEBUT = '//div[h3/text() = "Debut"]/div'
XPATH_PRIOR_FORMS = '//div[h3/a/text() = "Prior forms"]/div'
XPATH_NEXT_FORMS = '//div[h3/a/text() = "Next forms"]/div'
XPATH_PARTNERS = '//div[h3/text() = "Partners"]/div'
XPATH_VOICE_ACTORS = '//div[h3/text() = "Voice actors"]/div | //div[h3/text() = "Voice actor(s):"]/div'
XPATH_CARDS = '//div[h3/text() = "Cards"]/div | //div[h3/text() = "Card numbers:"]/div'
XPATH_OTHER_NAME = '//table[caption/text() = "Other Names"]/tbody'
XPATH_GROUPS = '//table[caption/text() = "Groups"]/tbody'
XPATH_VARIATIONS ='//table[caption/text() = "Variations"]/tbody'
XPATH_XPATH_DIGI_FUSE_FORMS = '//div[h3/a/text() = "DigiFuse forms"]/div'
XPATH_SLIDE_FORMS = '//div[h3/a/text() = "Slide forms"]/div'

XPATH_APPEARS_IN = '//div[h3/text() = "Appears in:"]/div'
XPATH_FIRST_APEARENCE = '//div[h3/text() = "First appearance:"]/div'
XPATH_LAST_APEARENCE = '//div[h3/text() = "Last appearance:"]/div'
XPATH_TRAITS = '//div[h3/text() = "Trait(s):"]/div'
XPATH_GENDER = '//div[h3/text() = "Gender:"]/div'
XPATH_ALIASES = '//div[h3/text() = "Aliases:"]/div'

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
        l = ItemLoader(DigimonItem(), response)
        l.add_xpath('name', XPATH_NAME)
        l.add_xpath('original_name', XPATH_ORIGINAL_NAME)
        l.add_xpath('image', XPATH_IMAGE)
        l.add_value('url', response.request.url)
        l.add_xpath('title', XPATH_TITLE)
        l.add_xpath('level', XPATH_LEVEL)
        l.add_xpath('digi_types', XPATH_DIGIMON_TYPE)
        l.add_xpath('attributes', XPATH_ATTRIBUTES)
        l.add_xpath('family', XPATH_FAMILY)
        l.add_xpath('size', XPATH_SIZE)
        l.add_xpath('debut', XPATH_DEBUT)
        l.add_xpath('slide_forms', XPATH_SLIDE_FORMS)
        l.add_xpath('prior_forms', XPATH_PRIOR_FORMS)
        l.add_xpath('next_forms', XPATH_NEXT_FORMS)
        l.add_xpath('partners', XPATH_PARTNERS)
        l.add_xpath('voice_actors', XPATH_VOICE_ACTORS)
        l.add_xpath('cards', XPATH_CARDS)
        l.add_xpath('other_names', XPATH_OTHER_NAME)
        l.add_xpath('variations', XPATH_VARIATIONS)
        l.add_xpath('groups', XPATH_GROUPS)

        yield l.load_item()

    def handle_errors(self):
        print("CENAS--------------------------------------------------------------------")