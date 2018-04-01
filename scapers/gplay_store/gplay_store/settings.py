# -*- coding: utf-8 -*-

# Scrapy settings for gplaycrawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'gplay_store'

SPIDER_MODULES = ['gplay_store.spiders']
NEWSPIDER_MODULE = 'gplay_store.spiders'
CONCURRENT_REQUESTS_PER_DOMAIN = 12
CONCURRENT_REQUESTS = 12
ITEM_PIPELINES = {
    'gplay_store.pipelines.GplayPipeline': 1
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Alo Ventures (+http://alo.ventures)'

REACTOR_THREADPOOL_MAXSIZE = 20
LOG_LEVEL = 'INFO'
COOKIES_ENABLED = False
##RETRY_ENABLED = False
DOWNLOAD_TIMEOUT = 60
##REDIRECT_ENABLED = False
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
