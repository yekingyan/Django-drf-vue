import json

import requests

from demo.settings import API_KEY, yunpian_text
# from demo.demo import local_settings
#
# API_KEY = local_settings.API_KEY
# yunpian_text = local_settings.yunpian_text

class YunPian(object):

    def __init__(self):
        self.api_key = API_KEY
        self.single_url = 'https://sms.yunpian.com/v2/sms/single_send.json'

    def send_sms(self, code, mobile):
        """
        发单条短信
        云片文档：https://www.yunpian.com/doc/zh_CN/domestic/single_send.html
        :return: True 发送成功， False 发送失败
        """
        parmas = {
            'apikey': self.api_key,
            'mobile': mobile,
            'text': yunpian_text(code),
        }
        response = requests.post(self.single_url, data=parmas)
        res_dict = json.loads(response.text)
        if res_dict.get(code) != 0:
            # 发送成功
            return True, res_dict.get('msg')
        return False, res_dict.get('msg')


if __name__ == '__main__':
    y = YunPian()
    y.send_sms(2020, 13246855446)
