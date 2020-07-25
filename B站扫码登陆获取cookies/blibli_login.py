import json
import os
import qrcode
import requests
from concurrent.futures import ThreadPoolExecutor
import time
import cv2 as cv


class Login:
    def __init__(self):
        self.oauthKey = ''
        self.qrcodeUrl = ''
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://passport.bilibili.com/',
            'Origin': 'https://passport.bilibili.com',
            'Connection': 'keep-alive'
        }
        self.session = requests.session()
        self.session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 '
                                                   'Firefox/62.0'})

    def responed(self, method, url, decode_level=2, retry=10, timeout=15, **kwargs):
        if method in ['get', 'post']:
            for _ in range(retry + 1):
                try:
                    response = getattr(self.session, method)(url, timeout=timeout, **kwargs)
                    return response.json() if decode_level == 2 else response.content if decode_level == 1 else response
                except:
                    pass
        return None

    def getqrcode(self):
        response = self.responed('get',"https://passport.bilibili.com/qrcode/getLoginUrl")
        if response and response.get('code') == 0:
            self.oauthKey = response['data']['oauthKey']
            self.qrcodeUrl = response['data']['url']
            print(self.oauthKey, self.qrcodeUrl)
            return True
        return False

    @staticmethod
    def showQRCode(url):
        try:
            cv.destroyAllWindows()
        except:
            pass
        qrCode = qrcode.QRCode()
        qrCode.add_data(url)
        qrCode = qrCode.make_image()
        qrCode.save("qrCode.png")
        img = cv.imread("qrCode.png", 1)
        cv.imshow("Login", img)
        cv.waitKey()

    def login(self):
        pool = ThreadPoolExecutor(max_workers=2)
        if self.getqrcode():
            pool.submit(self.showQRCode, self.qrcodeUrl)
            while True:
                time.sleep(1)
                data = {
                    'oauthKey': self.oauthKey,
                    'gourl': "https://passport.bilibili.com/account/security"
                }
                req = self.responed('post', "https://passport.bilibili.com/qrcode/getLoginInfo", data=data)
                if req['data'] == -4:
                    pass
                elif req['data'] == -2:
                    self.getqrcode()
                    pool.submit(self.showQRCode, self.qrcodeUrl)
                elif req['data'] == -5:
                    pass
                else:
                    break
            cookiesRaw = req['data']['url'].split('?')[1].split('&')
            cookies = {}
            for cookie in cookiesRaw:
                key, value = cookie.split('=')
                if key != "gourl" and key != "Expires":
                    cookies[key] = value
            print(json.dumps(cookies))
            os._exit(0)


if __name__ == '__main__':
    login = Login()
    login.login()
