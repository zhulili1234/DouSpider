# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest, Request
import urllib


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['douban.com']
    start_urls = ["https://www.douban.com/"]
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        "Cookie": "BAIDUID=B996F04451EC77E5101D453FE9B3FC40:FG=1; BIDUPSID=B996F04451EC77E5101D453FE9B3FC40; PSTM=1507804543; BDRCVFR[Fc9oatPmwxn]=G01CoNuskzfuh-zuyuEXAPCpy49QhP8; H_PS_PSSID=1425_21116_24022_22157"
    }

    def start_requests(self):
        return [
            Request("https://accounts.douban.com/login", callback=self.Login, meta={"cookiejar":1})]

    def Login(self, response):
        captcha = response.xpath("//img[@id='captcha_image']/@src").extract()
        if (len(captcha)>0):
            localpath = "C:/SpiderProgram/DouSpider/captcha.jpg"
            urllib.urlretrieve(captcha[0], filename=localpath)
            print (u"打开图片文件夹，查看验证码，请输入")
            #输入时要加双引号
            captcha_value = input()
            captcha_value = str(captcha_value)
            data = {
                "form_email":"15736933982",
                "form_password":"zhulili1995",
                "captcha-solution": captcha_value,
            }
            print(u"正在登陆中……")
            return [FormRequest.from_response(response,
                                              meta={"cookiejar": response.meta["cookiejar"]},
                                              headers=self.headers,
                                              formdata=data,
                                              callback=self.crawlerdata,
                                              )]

    def crawlerdata(self, response):
        print(u"完成登录.........")
        title = response.xpath("/html/head/title/text()").extract()
        content2 = response.xpath("//meta[@name='description']/@content").extract()
        print ">>>>>>>>", title, content2

    def parse(self, response):
        pass
