import re
import html2text
from scrapy import Item, Field
from scrapy.loader.processors import Identity, TakeFirst, MapCompose
from scrapy.loader import ItemLoader

h = html2text.HTML2Text()
h.ignore_links = True
h.ignore_emphasis = True

def replace_special_characters(text):
    text = re.sub(r'##', '', text)
    text = re.sub('\\\\', '', text)
    text = re.sub('• ', '', text)

    return text

def break_on_newline(text):
    return text.split('\n')

def remove_reference_link_from_strings(text):
    return re.sub(r'\[\d*\]', '', text)

def remove_whitespace(text):
    return text.strip()

def filter_empty_strings(text):
    return None if len(text) == 0 else text

class DigimonItemLoader(ItemLoader):
    default_input_processor = MapCompose(
        h.handle, 
        replace_special_characters, 
        remove_reference_link_from_strings, 
        break_on_newline, 
        remove_whitespace, 
        filter_empty_strings
    )

    name_in = Identity()
    name_out = TakeFirst()

    original_name_in = Identity()
    original_name_out = Identity()

    image_in = Identity()
    image_out = TakeFirst()

    url_in = Identity()
    url_out = TakeFirst()


class DigimonItem(Item):
    name = Field()
    original_name = Field()
    image = Field()
    url = Field()
    title = Field()
    level = Field()
    digi_types = Field()
    attributes = Field()
    family = Field()
    size = Field()
    debut = Field()
    slide_forms = Field()
    prior_forms = Field()
    next_forms = Field()
    partners = Field()
    voice_actors = Field()
    cards = Field()
    other_names = Field()
    variations = Field()
    groups = Field()
