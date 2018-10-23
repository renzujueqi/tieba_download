# coding=utf-8
import time
import scrapy
from scrapy.http import Request
from p1.items import P1Item



class bai_du_news(scrapy.spiders.Spider):
    name = "baidu"
    allowed_domains = ["baidu.com"]
    start_urls = [
        "http://tieba.baidu.com/f?kw=%E6%98%9F%E5%BA%A7&ie=utf-8&pn=0"
    ]

    def start_requests(self):

        # 星座吧全量
        start_url_list = [
            # "http://tieba.baidu.com/f?kw=%E6%98%9F%E5%BA%A7",
            # "https://tieba.baidu.com/f?kw=%E5%A4%A9%E8%9D%8E%E5%BA%A7",
            # "https://tieba.baidu.com/f?kw=%E5%8F%8C%E9%B1%BC%E5%BA%A7",
            # "https://tieba.baidu.com/f?kw=%E6%B0%B4%E7%93%B6%E5%BA%A7",
            # "https://tieba.baidu.com/f?kw=%E5%A4%A9%E7%A7%A4%E5%BA%A7",
            # "https://tieba.baidu.com/f?kw=%E5%8F%8C%E5%AD%90%E5%BA%A7",
            # "https://tieba.baidu.com/f?kw=%E5%A4%84%E5%A5%B3%E5%BA%A7",
            # "https://tieba.baidu.com/f?kw=%E7%8B%AE%E5%AD%90%E5%BA%A7",
            # "https://tieba.baidu.com/f?kw=%E5%B7%A8%E8%9F%B9%E5%BA%A7",
            # "https://tieba.baidu.com/f?kw=%E5%B0%84%E6%89%8B%E5%BA%A7",
            # "https://tieba.baidu.com/f?kw=%E7%99%BD%E7%BE%8A%E5%BA%A7",
            # "https://tieba.baidu.com/f?kw=%E9%87%91%E7%89%9B%E5%BA%A7",
            # "https://tieba.baidu.com/f?kw=%E9%AD%94%E7%BE%AF%E5%BA%A7"
            
            # "http://tieba.baidu.com/f?kw=%E9%A3%8E%E6%99%AF",
            # "http://tieba.baidu.com/f?kw=%E6%97%85%E8%A1%8C",
            # "http://tieba.baidu.com/f?kw=%E6%97%85%E6%B8%B8",
            # "http://tieba.baidu.com/f?kw=%E9%A9%B4%E5%8F%8B",
            # "http://tieba.baidu.com/f?kw=%E8%83%8C%E5%8C%85%E5%AE%A2"

            "https://tieba.baidu.com/f?kw=%E7%BE%8E%E5%A5%B3",
            "https://tieba.baidu.com/f?kw=%E6%83%85%E4%BE%A3",
            "https://tieba.baidu.com/f?kw=%E5%A5%B3%E7%A5%9E",
            "https://tieba.baidu.com/f?kw=%E8%90%8C%E5%A6%B9%E5%AD%90",
            "https://tieba.baidu.com/f?kw=%E7%BC%A4%E7%BA%B7%E7%AB%A5%E5%B9%B4",
            "https://tieba.baidu.com/f?kw=%E6%83%85%E4%BA%BA%E8%8A%82",
            "https://tieba.baidu.com/f?kw=%E6%83%85%E6%84%9F",
            "https://tieba.baidu.com/f?kw=%E5%AF%82%E5%AF%9E",
            "https://tieba.baidu.com/f?kw=%E5%BF%83%E6%83%85",
            "https://tieba.baidu.com/f?kw=%E6%84%9F%E6%83%85"


        ]
        for head_url in start_url_list:
            print(head_url)
            for ii in range(500):
                end = "&ie=utf-8&pn=" + str(ii*50)
                fu_url = head_url + str(end)
                yield scrapy.Request(fu_url, callback=self.parse)


    def parse(self, response):
        # print(response, type(response))
        # from scrapy.http.response.html import HtmlResponse
        # print(response.body_as_unicode())
        base_url = 'http://tieba.baidu.com'
        all_li_element = response.css('li')
        for li_itm in all_li_element:
            futher_url = li_itm.css('a')
            if len(futher_url) > 0:
                # f_url = futher_url[0].css('a::attr(href)').extract()
                if len(futher_url[0].css('a::attr(href)').extract()) > 0:
                    f_url = f_url = futher_url[0].css('a::attr(href)').extract()[0]
                    f_url = f_url.replace("//", "/")
                    f_url = base_url + f_url
                    print(f_url)
                    for ii in range(1,10):
                        end = "?pn=" + str(ii)
                        f_url = f_url + end
                        if "/p/" in f_url:
                            yield Request(url=f_url, callback=self.parse_floor_data)



    def parse_floor_data(self, response):
        """抽取详细页上各个楼层的文本"""
        itm = P1Item()
        all_floor = response.css('div.l_post.j_l_post.l_post_bright')
        for floor in all_floor:
            c = floor.css('div.p_content')[0].css('cc')
            text = c[0].css("div").css("::text").extract()[0]
            text = text.strip()
            if len(text) == 0:
                text = c.css('::text').extract()[0]
            text = text.strip()
            print(text)
            itm["speak"] = text
            time.sleep(0.02)
            yield itm

