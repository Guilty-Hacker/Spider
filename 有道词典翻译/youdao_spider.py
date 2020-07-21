import requests
import json
from time import sleep, time
import random
import hashlib


# MD5加密
def md5(value):
    decode_md5 = hashlib.md5()
    decode_md5.update(value.encode('utf-8'))
    return decode_md5.hexdigest()


def form_data(string):
    e = string
    ts = round(time())
    # print(ts)
    salt = str(ts) + str(random.randint(0, 9))
    # print(salt)
    bv = md5(
        "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36")
    sign = md5("fanyideskweb" + e + salt + "mmbP%A-r6U3Nw(n]BjuEU")
    data = {
        'i': e,
        'from': 'AUTO',
        'to': 'AUTO',
        'smartresult': 'dict',
        'client': 'fanyideskweb',
        'salt': salt,
        'sign': sign,
        'ts': ts,
        'bv': bv,
        'doctype': 'json',
        'version': '2.1',
        'keyfrom': 'fanyi.web',
        'action': 'FY_BY_REALTlME'
    }
    return data


def request_access(url, data):

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Content-Length': '237',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'OUTFOX_SEARCH_USER_ID=1648504734@10.169.0.83; OUTFOX_SEARCH_USER_ID_NCOO=1054516127.1065001; JSESSIONID=aaaFtapMs3Ow4bIaK06-w; ___rl__test__cookies=1580462241081',
        'DNT': '1',
        'Host': 'fanyi.youdao.com',
        'Origin': 'https://fanyi.youdao.com',
        'Referer': 'https://fanyi.youdao.com/',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    response = requests.post(url, headers=headers, data=data)
    return response


def main():
    url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
    e = input('请输需翻译的内容:')
    data = form_data(e)
    translate = request_access(url, data=data)
    #    提取json数据
    print(translate.json()['translateResult'][0][0]['tgt'])
    # print(translate.text)


if __name__ == '__main__':
    while True:
        main()



