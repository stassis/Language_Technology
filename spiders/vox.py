# -*- coding: utf-8 -*-
#from time import sleep
import scrapy
import uuid #uuid3 = MD5 hash || uuid5 = SHA-1 hash

class VoxSpider(scrapy.Spider):
    name = 'vox'
    #important to have 'vox.com' as allowed_domain. Otherwise will not work, if ex. we had 'vox.com/news'
    allowed_domains = ['vox.com']
    start_urls = ['http://vox.com/news/']

    #extract links from articles from each page
    def parse(self, response):
        for link in response.xpath('//h2[@class="c-entry-box--compact__title"]/a/@href').extract():
            yield scrapy.Request(link,callback=self.parse_contents) 

        #extract link of 'next' button
        next_page = response.xpath('//*[contains(@class,"c-pagination__next")]/@href').extract_first()
        if next_page:
            #link of 'next' button is incomplete, so we create a full URL
            url = 'https://www.vox.com' + next_page
            #absolute_next_page = response.urljoin(next_page)
            yield scrapy.Request(url)
            #sleep(1) sleep 1 sec each page, so that we don't get blocked from scraping vox.com

    #on each article we scrape URL, title and contents
    def parse_contents(self, response):
        title = response.xpath('//h1/text()').extract_first()
        content = response.xpath('//*[@class="c-entry-content "]/p').extract()
        url = response.url
        encoded_url = uuid.uuid3(uuid.NAMESPACE_URL, url) #hash url in order to achieve uniqness
        
        #unify all seperate-paragraph elements into a single element
        con = ""
        for i in range(0,len(content)):
            con = con + content[i]
        
        if con and title:
            yield{
                'Hash': encoded_url,
                'Title': title,
                'Content': con,
                'URL': url
            }           
        