# -*- coding: utf-8 -*-

# Scrapy settings for gplaycrawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
from datetime import datetime
import logging
import os

GP_FOLDER = os.path.dirname(os.path.realpath(__file__))

# Create directories
if not os.path.exists(GP_FOLDER + '/logs/'):
    os.makedirs(GP_FOLDER + '/logs/')

if not os.path.exists(GP_FOLDER + '/html/'):
    os.makedirs(GP_FOLDER + '/html/')

if not os.path.exists(GP_FOLDER + '/html/failed_scrapes'):
    os.makedirs(GP_FOLDER + '/html/failed_scrapes')


logging.basicConfig(format='%(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)
fh = logging.FileHandler(GP_FOLDER + '/logs/log.txt')
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)

DATEID = datetime.now().strftime("%Y-%m-%d")

BOT_NAME = 'gplay_store'

SPIDER_MODULES = ['gplay_store.spiders']
NEWSPIDER_MODULE = 'gplay_store.spiders'
CONCURRENT_REQUESTS_PER_DOMAIN = 12
CONCURRENT_REQUESTS = 12
ITEM_PIPELINES = {
    'gplay_store.pipelines.GplayPipeline': 1
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'devin wieker'

REACTOR_THREADPOOL_MAXSIZE = 20
LOG_LEVEL = 'INFO'
COOKIES_ENABLED = False
##RETRY_ENABLED = False
DOWNLOAD_TIMEOUT = 60
##REDIRECT_ENABLED = False
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1

DB_USERNAME = 'devinwieker'
DB_PASSWORD = 'password'
DB_ENDPOINT = 'pc.cq63rozymplk.us-east-1.rds.amazonaws.com'
DB_NAME = 'PC'
DB_PORT = 3306
