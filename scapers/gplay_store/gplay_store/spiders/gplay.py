import re
from dateutil import parser
from scrapy import Request, Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from gplay_store.utils.strings import *
from bs4 import BeautifulSoup
import gplay_store.config as CONFIG


class PlayStoreSpider(CrawlSpider):
    '''Google Play Store Spider'''
    name = 'gplay'

    start_urls = ['https://play.google.com/store/apps/']
    rules = [
        Rule(
            LinkExtractor(
                allow=('/store/apps/details'),
                deny=('followup')
            ),
            callback='parse_app',
            follow=True
        ),
        Rule(
            LinkExtractor(allow=('/store/apps/')),
            follow=True
        ),
    ]

    def parse_app(self, response):
        '''Parse specific app details'''
        try:
            soup = BeautifulSoup(response.text, 'lxml')
            item = {}
            item['name'] = soup.find(itemprop='name').text
            item['name'] = bytes(item['name'], 'utf-8').decode('utf-8','ignore')
            item['genre'] = soup.find(itemprop='genre').text
            exp = re.compile(r'[^\d.]+')
            item['price'] = float(exp.sub('',soup.find(itemprop='price')['content']))
            item['description'] = soup.find(itemprop='description')['content']
            try:
                item['rating'] = float(soup.find(itemprop='ratingValue')['content'])
                item['rating_count'] = int(soup.find(itemprop='ratingCount')['content'])
            except:
                item['rating'] = None
                item['rating_count'] = None
            for div in soup.find_all('div', {'class':'hAyfc'}):
                key, value = div.div.text, div.span.text
                if key == 'Size':
                    try:
                        item['size'] = app_size_string_to_float(value)
                    except ValueError:
                        item['size'] = None
                if key == 'Installs':
                    item['installs'] = int(re.sub("[^0-9]", "", value))
                if key == 'Current Version':
                    item['version'] = value
                if key == 'Updated':
                    item['page_update_time'] = value
            item['appid'] = response.url.split('?id=')[-1]
            item['ID'] = hash(item['appid'])
            return item
        except Exception as e:
            CONFIG.logger.error(response.url + ' failed: ' + str(e))
            fname = response.url.split('?id=')[-1].replace('.', '_')
            with open(CONFIG.GP_FOLDER + '/html/failed_scrapes/' + fname , 'w+') as f:
                f.write(response.text)
