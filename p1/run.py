# coding=utf-8
from scrapy import cmdline

name = 'baidu'  #spider name

cmd = 'scrapy crawl {0}'.format(name)

cmdline.execute(cmd.split())
