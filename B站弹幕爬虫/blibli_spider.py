import requests
from lxml import etree
import re


class BilibiliSpider:
    def __init__(self, bv):
        self.bv_url = "https://m.bilibili.com/video/" + bv
        self.headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) "
                                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Mobile "
                                      "Safari/537.36"}

    def get_cid(self):
        response = requests.get(self.bv_url, headers=self.headers)
        cid = re.findall('cid:(.*?),', response.text)[0].strip()
        return cid

    def get_bullet_chat(self, cid):
        response = requests.get('https://api.bilibili.com/x/v1/dm/list.so?oid={}'.format(cid), headers=self.headers)
        # print(response.text)
        bullet = re.findall('<d p=".*?">(.*?)</d>', response.content.decode())
        # print(bullet)
        for chat in bullet:
            print(chat)

        print("共有弹幕:{}条".format(len(bullet)))
        return 1

    def run(self):
        cid = self.get_cid()
        text = self.get_bullet_chat(cid)


if __name__ == '__main__':
    bv_name = input('请输入要爬取的BV号:')
    spider = BilibiliSpider(bv_name)
    spider.run()
