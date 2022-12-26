# -*- coding: utf-8 -*-
"""
Created on Sat Aug 13 17:09:36 2022

@author: Dorina


TO RUN: scrapy runspider scrapy.py
"""

import scrapy
import pickle
import psycopg2
from urllib.parse import urlparse
from mastodontool import settings

with open("alive", "rb") as fp:   # Unpickling
    b = pickle.load(fp)
    
    
conn = psycopg2.connect(
    dbname=settings.DATABASES.get("default",{})["NAME"],
    user=settings.DATABASES.get("default",{})["USER"],
    password=settings.DATABASES.get("default",{})["PASSWORD"],
    host=settings.DATABASES.get("default",{})["HOST"],
)
cur = conn.cursor()

foundlist = []
 
class ScrapyTheSpider(scrapy.Spider):
    #name of the spider
    name = 'PythonGUI'
 
    #list of allowed domains
    #allowed_domains = ['mastodon.xyz']
    allowed_domains = b
 
    #starting url for scraping
    start_urls = []
    for i in b:
        start_urls.append("https://" + i + "/about/more")
        
    #start_urls = ['https://mastodon.xyz/about/more']
 
    #setting the location of the output csv file
    custom_settings = {
        'FEED_URI' : 'TempFolder/PythonGUI.csv'
    }
 
    def parse(self, response):
        #Remove XML namespaces
        response.selector.remove_namespaces()
 
        #Extract article information
        for row in response.xpath("//table/tbody/tr"):
            if row.xpath('td/span/text()').extract_first() != None:
                servers = {
                    'name' : row.xpath('td/span/text()').extract_first(),
                    }
            else:
                servers = {                    
                    'name' : row.xpath('td/text()').extract_first(),
                    }
                
            yield servers
            parsed_uri = urlparse(response.url)
            domain = '{uri.netloc}'.format(uri=parsed_uri)
            
            
            cur.execute("""INSERT INTO "banned" ("source", "banned") VALUES (%s, %s); """, (domain, servers['name']))
            conn.commit()
    


cur.close()
conn.close()
