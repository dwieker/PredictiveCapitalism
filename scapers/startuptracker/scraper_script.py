import re
from scrapy import Request, Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.parse import urlencode
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base, DeferredReflection
import time
from datetime import datetime
import os
import requests

DATEID = datetime.now().strftime("%Y-%m-%d")
Base = declarative_base(cls=DeferredReflection)
CATEGORIES = [
    'ADVERTISING', 'AI', 'ANALYTICS', 'AR/VR', 'ACCOUNTING AND LEGAL',
    'AUTOMOTIVE', 'BIG DATA', 'BIOTECH', 'BLOCKCHAIN', 'BOTS', 'COMMUNICATION',
    'CONSULTING', 'CONTENT', 'DATA', 'DESIGN', 'E COMMERCE', 'EDUCATION', 'ENERGY',
    'ENTERTAINMENT', 'EVENTS', 'FASHION', 'FINANCE', 'FOOD AND BEVERAGES', 'GAMING',
    'GOVERNMENTAL', 'HARDWARE', 'HEALTH', 'HOSPITALITY', 'HR AND RECRUITMENT', 'INSURANCE',
    'IOT', 'MANUFACTURING', 'MARKETING', 'MEDIA', 'MEDICAL', 'MESSAGING', 'MUSIC', 'PRODUCTIVITY',
    'REAL ESTATE', 'RETAIL', 'ROBOTICS', 'SALES', 'SECURITY', 'SHARING ECONOMY', 'SOCIAL NETWORKS',
    'SOFTWARE DEV', 'STARTUPS', 'TRAVEL', 'OTHER'
]
browser = webdriver.Chrome()

class StartupTracker(Base):
    __tablename__ = "dim_startuptracker"

sqlalchemy.String(1000, convert_unicode=True)

DB_USERNAME = 'devinwieker'
DB_PASSWORD = 'password'
DB_ENDPOINT = 'pc.cq63rozymplk.us-east-1.rds.amazonaws.com'
DB_NAME = 'PC'
DB_PORT = 3306
credentials = (
    DB_USERNAME,
    DB_PASSWORD,
    DB_ENDPOINT,
    DB_NAME,
)
db_uri = "mysql+pymysql://%s:%s@%s/%s?use_unicode=yes&charset=utf8mb4" % credentials
engine = sqlalchemy.create_engine(db_uri)
Base.prepare(engine)
Session = sessionmaker(bind=engine)
session = Session()

url = 'https://startuptracker.io/discover?filters%5B0%5D%5Bcc%5D%5Bq%5D=US&filters%5B1%5D%5Bbm%5D%5Bq%5D=ACCOUNTING%20AND%20LEGAL&page=0'
for cat in CATEGORIES:
    payload = {
        'filters[0][cc][q]': 'US',
        'filters[1][bm][q]': cat,
        'page': 0
    }
    cat_url = 'https://startuptracker.io/discover?' + urlencode(payload, True)
    response = requests.get(cat_url)
    soup = BeautifulSoup(response.text, 'lxml')
    pages = soup.find_all(attrs={'data-page':re.compile(r".*")})

    if len(pages) > 0:
        num_pages = int(max([item['data-page'] for item in pages])) + 1
    else:
        num_pages = 0

    for page in range(num_pages):
        payload = {
            'filters[0][cc][q]': 'US',
            'filters[1][bm][q]': cat,
            'page': page
        }
        cat_url = 'https://startuptracker.io/discover?' + urlencode(payload, True)
        response = requests.get(cat_url)
        soup = BeautifulSoup(response.content, 'lxml')
        links = ['https://startuptracker.io' + link['href'] for link in soup.find_all(href=re.compile(r'^/startups/'))]
        print("Number of links: ", len(links))
        print(links)
        for link in links:
            try:
                print("Parsing...", link)
                browser.get(link)
                browser.implicitly_wait(10)

                # Wait for the company webpage link to load
                browser.find_element_by_class_name('_w0x3akc')

                soup = BeautifulSoup(browser.page_source)
                data = {}
                for i, item in enumerate(soup.find_all(class_='_1xeadpo')):
                    subitems = [subitem.text for subitem in item.find_all('p')]
                    if i == 0:
                        data['founded_date'] = subitems[0] + ' ' + subitems[1]
                    elif i == 1:
                        data['location'] = subitems[0] + ' ' + subitems[1]
                    elif subitems[1] == 'pageviews p.m.':
                        data['monthly_pageviews'] = subitems[0]
                    elif subitems[1] == 'in team':
                        data['team_members'] = subitems[0]
                    elif subitems[1] == 'amount raised':
                        data['amount_raised'] = subitems[0]
                    elif subitems[1] == 'global rank':
                        data['global_rank'] = subitems[0]
                    else:
                        data[subitems[1]] = subitems[0]
                data['markets'] = '__'.join([item.text for item in soup.find_all(class_='_14jrgnk8')])
                data['products'] = '__'.join([item.text for item in soup.find_all(class_='_sz431i8')])
                data['revenue_model'] = [item.text for item in soup.find_all(class_='_1sj8tpk8')]
                data['website'] = soup.find(class_='_w0x3akc')['href']
                data['description'] = soup.find(class_='_qgzmqh').text
                data['name'] = soup.find(class_='_1vj0t0j').text
                data['url'] = link
                data['category'] = cat
                data['ds'] = DATEID

                try:
                    session.bulk_insert_mappings(StartupTracker, [data])
                    session.commit()
                except Exception as e:
                    session.rollback()
                    print(e)
            except Exception as e:
                print(e)
