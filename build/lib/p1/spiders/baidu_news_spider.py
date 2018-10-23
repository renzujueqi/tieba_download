# coding=utf-8
import scrapy
from scrapy.http import Request

class bai_du_news(scrapy.spiders.Spider):
    name = "baidu"
    allowed_domains = ["baidu.com"]
    start_urls = [
        "http://tieba.baidu.com/f?kw=%E6%98%9F%E5%BA%A7",
    ]


    def parse(self, response):
        # print(response, type(response))
        # from scrapy.http.response.html import HtmlResponse
        # print(response.body_as_unicode())
        base_url = 'http://tieba.baidu.com'
        all_li_element = response.css('li')
        for li_itm in all_li_element:
            futher_url = li_itm.css('a')
            if len(futher_url) > 0:
                f_url = futher_url[0].css('a::attr(href)').extract()
                f_url = f_url.replace("//", "/")
                print(f_url)
                yield Request(url=f_url, callback=self.parse_floor_data)



    def parse_floor_data(self, response):
        """抽取详细页上各个楼层的文本"""
        all_floor = response.css('div.l_post.j_l_post.l_post_bright')
        for floor in all_floor:
            c = floor.css('div.p_content')[0].css('cc')
            text = c.css('::text').extract()[0]
            print(text)

