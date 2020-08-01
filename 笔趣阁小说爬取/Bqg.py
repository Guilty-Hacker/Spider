from bs4 import BeautifulSoup
import requests
import sys


class Bqg_Spider:
    def __init__(self):
        self.url = 'http://www.biqukan.com/'
        self.chapter_url = 'https://www.biqukan.com/72409_72409669/'
        self.names = []
        self.urls = []
        self.nums = []

    def get_download_url(self):
        response = requests.get(self.chapter_url)
        html = response.content.decode('gbk')
        analysis = BeautifulSoup(html,'lxml')
        list_main = analysis.find_all('div',class_='listmain')
        a_list = BeautifulSoup(str(list_main[0]),'lxml')
        # print(list_main)
        a = a_list.find_all('a')
        # print(a)
        self.nums = len(a[15:])
        for each in a[12:]:
            # print(each)
            self.names.append(each.string)
            self.urls.append(self.url + each.get('href'))

    def get_content(self, url):
        response = requests.get(url)
        html = response.content.decode('gbk')
        analysis = BeautifulSoup(html,'lxml')
        texts = analysis.find_all('div', class_='showtxt')
        texts = texts[0].text.replace('\xa0'*8, '\n\n')
        return texts

    def write(self, path, name,text):
        with open(path + '.txt', 'a', encoding='utf-8') as f:
            f.write(name + '\n')
            f.writelines(text)
            f.write('\n\n')


if __name__ == '__main__':
    down = Bqg_Spider()
    down.get_download_url()
    for i in range(down.nums):
        down.write(down.names[i], '张凡神医.txt', down.get_content(down.urls[i]))
        sys.stdout.write("  已下载:%.3f%%" % float(i/down.nums*100) + '\r')
        sys.stdout.flush()