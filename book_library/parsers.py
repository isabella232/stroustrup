# -*- coding: utf-8 -*-
author = 'Roman Usynin'
email = 'r.usynin@crystalnix.com'
copyright = 'Copyright 2014, Crystalnix'

from urllib2 import urlopen
from amazon.api import AmazonAPI, AsinNotFound
from re import search
from bs4 import BeautifulSoup
from django.conf import settings
from urlparse import urlparse


class BaseParser(object):
    def __init__(self):
        self.title = ''
        self.authors = ''
        self.book_image_url = ''
        self.price = ''
        self.description = ''

    def parse(self, urlopen_object):
        raise NotImplementedError()


class AmazonParser(BaseParser):
    def parse(self, urlopen_object):
        product_url = search('http://www.amazon.com/([\\w-]+/)?(dp|gp/product)/(\\w+/)?(\\w{10})', urlopen_object.url)
        if product_url is not None:
                id_product = product_url.group(4)
                amazon = AmazonAPI(settings.AMAZON_ACCESS_KEY, settings.AMAZON_SECRET_KEY, settings.AMAZON_ASSOC_TAG)
                product = amazon.lookup(ItemId=id_product)
                self.title = product.title
                self.authors = u", ".join(unicode(v) for v in product.authors)
                self.price = '{0} {1}'.format(product.price_and_currency[0], product.price_and_currency[1])
                self.description = product.editorial_review
                if product.medium_image_url is None:
                    self.book_image_url = ''
                else:
                    self.book_image_url = product.medium_image_url
                return self

        else:
            return None


class OzonParser(BaseParser):
    def parse(self, urlopen_object):
        try:
            soup = BeautifulSoup(urlopen_object.read().replace('\n', '').decode('windows-1251'))
            self.title = soup.find("h1").text
            self.authors = soup.find("p", itemprop="author").text.split(':')[1]
            self.book_image_url = soup.find("img", attrs={'class': "eMicroGallery_fullImage"}).attrs['src']
            self.price = soup.find("span", attrs={'itemprop': 'price', 'class': 'hidden'}).text
            self.description = soup.find("div", id="detail_description").text.replace(u"Сообщить о неточности в описании",'')
            return self
        except:
            return None


#factory pattern
def book_shop_factory(url):
    name_shop = urlparse(url)[1].split('.')[1]
    shops = {
        'amazon': AmazonParser,
        'ozon': OzonParser,
    }
    if name_shop in shops:
        return shops[name_shop]()
    else:
        return None