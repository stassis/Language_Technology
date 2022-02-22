# -*- coding: utf-8 -*-
import scrapy
from time import sleep
import uuid #uuid3 = MD5 hash || uuid5 = SHA-1 hash

class F1Spider(scrapy.Spider):
    name = 'f_1'
    allowed_domains = ['theguardian.com']
    start_urls = ['http://theguardian.com/sport/formulaone/']

    def parse(self, response):
        
        for link in response.xpath('//div[@class="fc-item__content "]//a/@href').extract():
                yield scrapy.Request(link,callback=self.parse_f1_contents)

        #extract link of 'next' button
        next_page = response.xpath('//a[contains(@rel,"next")]/@href').extract_first()
        if next_page:
            #absolute_next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page)
            sleep(5) #sleep 5 sec each page, so that we don't get blocked from scraping guardian.com         

    
    
    #on each guardian article we scrape the title and the contents
    def parse_f1_contents(self, response):
        title = response.xpath('//h1/text()').extract_first()
        content = response.xpath('//*[contains(@id,"maincontent")]//div/p').extract()

        #unify all seperate-paragraph elements into a single element
        con = ""
        for i in range(0,len(content)):
            con = con + content[i]
        
        #check if there exists title && content, and return tuples that contain both. In some cases title && content don't exist
        if con and title:
            url = response.url
            encoded_url = uuid.uuid3(uuid.NAMESPACE_URL, url) #hash url in order to achieve uniqness

            yield{
                'Hash': encoded_url,
                'Title': title,
                'Content': con,
                'URL': url
            }                         
