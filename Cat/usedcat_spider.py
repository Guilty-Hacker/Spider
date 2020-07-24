import asyncio
import aiohttp
from lxml import etree
"""
使用时应该改User-Agent以及Cookie
"""

NUM = 5


class Cat:
    def __init__(self):
        self.num = asyncio.Semaphore(NUM)
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7',
            # 'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Cookie': 'antipas=4918R320646f722036U294S27; uuid=9a0d0bff-c55f-4632-aef6-ca42856e0d81; ganji_uuid=7952110987853881632587; lg=1; cainfo=%7B%22ca_a%22%3A%22-%22%2C%22ca_b%22%3A%22-%22%2C%22ca_s%22%3A%22self%22%2C%22ca_n%22%3A%22self%22%2C%22ca_medium%22%3A%22-%22%2C%22ca_term%22%3A%22-%22%2C%22ca_content%22%3A%22-%22%2C%22ca_campaign%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22scode%22%3A%22-%22%2C%22keyword%22%3A%22-%22%2C%22ca_keywordid%22%3A%22-%22%2C%22display_finance_flag%22%3A%22-%22%2C%22platform%22%3A%221%22%2C%22version%22%3A1%2C%22client_ab%22%3A%22-%22%2C%22guid%22%3A%229a0d0bff-c55f-4632-aef6-ca42856e0d81%22%2C%22ca_city%22%3A%22heze%22%2C%22sessionid%22%3A%22c8e1844d-ab76-449d-dae3-0ca9ea3d0d39%22%7D; cityDomain=cs; clueSourceCode=%2A%2300; user_city_id=204; preTime=%7B%22last%22%3A1595597858%2C%22this%22%3A1595428201%2C%22pre%22%3A1595428201%7D; sessionid=86675f44-285f-40e2-fc92-03084a0bb356',
            # 'DNT': '1',
            'Host': 'www.guazi.com',
            # 'Pragma': 'no-cache',
            'Referer': 'https://www.guazi.com/cs/buy/o1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
        }

    async def scrape(self, url):
        async with self.num:
            async with aiohttp.ClientSession(headers=self.headers).get(url) as response:
                await asyncio.sleep(1)
                return await response.text()

    async def index(self, page):
        url = f'https://www.guazi.com/cs/buy/o{page}'
        html = await self.scrape(url)
        await self.parse(html)

    async def parse(self, html):
        with open('car.csv', 'a+', encoding='utf-8') as f:
            doc = etree.HTML(html)
            # print(html)
            selector = doc.xpath('//ul[@class="carlist clearfix js-top"]/li')
            for cat in selector:
                name = cat.xpath('a/h2/text()')[0]
                details = cat.xpath('a/div[1]/text()')
                date = details[0]
                distance = details[1]
                service = details[2]
                price = cat.xpath('a/div[2]/p/text()')[0]
                data = f'{name},{date},{distance},{service},{price}\n'
                f.write(data)

    async def main(self):
        scrape_index = [asyncio.ensure_future(self.index(page)) for page in range(5)]
        await asyncio.gather(*scrape_index)


if __name__ == '__main__':
    spider = Cat()
    asyncio.get_event_loop().run_until_complete(spider.main())
