# -*- coding: utf-8 -*-
import scrapy
import os
import re

from ..items import MspatchItem

class MspatchSpider(scrapy.Spider):
    name = 'mspatch'
    allowed_domains = ['www.catalog.update.microsoft.com']
    start_urls = ['http://www.catalog.update.microsoft.com/Search.aspx?q=MS12-020']

    def parse(self, response):

        # json_urls = response.xpath('//table[@data-testid="vuln-feed-table"]/tbody/tr[re:test(@data-testid,"vuln-json-feed-row-*gzip*")]/td[1]/a/@href').extract()
        # print json_urls
        querykey = response.url.split('=')[-1]
        if not os.path.exists(querykey):
            os.mkdir(querykey)
        trarr = response.xpath('//div[@id="tableContainer"]/table/tr')
        for tr in trarr:

            if tr.xpath('@id').extract_first() == "headerRow":
                print "header"
                continue
            title = tr.xpath('td[2]/a/text()').extract_first().replace('\n','').strip()
            id = tr.xpath('@id').extract_first().split('_')[0]
            print title,id,str(id)
            formdata={
                'updateIDs': "[{'size': 0, 'languages': '', 'uidInfo': '%s','updateID': '%s'}]"%(id,id)
            }
            # print formdata
            yield scrapy.FormRequest(url="http://www.catalog.update.microsoft.com/DownloadDialog.aspx",formdata=formdata,
                                     meta={'title':title,"querykey" : querykey},
                                     callback=self.download_page)
            # break

    def download_page(self,response):
        print "====>"
        title =  response.meta['title']
        querykey = response.meta['querykey']
        # print response.text
        index = 0
        res_text = response.text.encode('utf-8')
        while(True):
            downloadurl_split = 'downloadInformation[0].files[{}].url = \''.format(index)
            # downloadInformation[0].files[0].longLanguages = 'all';
            res_text.find(downloadurl_split)
            if downloadurl_split in res_text:

                downloadurl = res_text.split(downloadurl_split)[1].split('\';')[0]
                language_split = 'downloadInformation[0].files[{}].longLanguages = \''.format(index)
                language = res_text.split(language_split)[1].split('\';')[0]
                print downloadurl
                item = MspatchItem()
                item['file_urls'] = [downloadurl]
                item['patch_title'] = querykey
                item['title'] = title
                item['language'] = language
                yield item
            else:
                print 'downurl is null'
                break

            index +=1
        # print response.header