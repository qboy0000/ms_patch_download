# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.conf import settings
from scrapy.pipelines.files import FilesPipeline
import os,shutil

def mymovefile(srcfile,dstfile):
    if not os.path.isfile(srcfile):
        print "%s not exist!"%(srcfile)
    else:
        shutil.move(srcfile,dstfile)          #移动文件
        print "move %s -> %s"%( srcfile,dstfile)

class MspatchPipeline(FilesPipeline):
    def __init__(self, store_uri, download_func=None, settings=None):

        super(MspatchPipeline, self).__init__(store_uri=store_uri, download_func=download_func, settings=settings)

    # def file_path(self, request, response=None, info=None):
    #     print request.url
    #     return request.url

    def item_completed(self, results, item, info):

        # print "item_completed==>",results,item
        # col = self.db['cvebase']
        for (r,dict) in results:
            if r:
                dst_dir = os.path.join(item['patch_title'],item['title'])
                if not os.path.exists(dst_dir):
                    os.mkdir(dst_dir)
                if item['language'] != "all":
                    dst_dir = os.path.join(dst_dir,item['language'])
                    if not os.path.exists(dst_dir):
                        os.mkdir(dst_dir)
                filename = dict['url'].split('/')[-1]
                dst_file = os.path.join(dst_dir,filename)
                src_file = os.path.join(self.store.basedir, dict['path'])
                if not os.path.isfile(src_file):
                    print "download item fail",results,dst_file
                else:
                    shutil.move(src_file, dst_file)
            else:
                print item['patch_title'],item['title'],'download error'

        return item
