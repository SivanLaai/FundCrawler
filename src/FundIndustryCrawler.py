from Config import *
import requests
import json
from DataControl import dataControl
import execjs
from lxml import etree
from io import StringIO, BytesIO
from urllib.parse import unquote, quote
from Logger import logger
import time

header_str = '''Host:api.fund.eastmoney.com
Proxy-Connection:keep-alive
User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.76
Accept:*/*
Referer:http://fundf10.eastmoney.com/
Accept-Encoding:gzip, deflate
Accept-Language:zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7'''


params_str = '''fundCode=002190
year=
callback=jQuery1830379581891375977_1618539483467
_=1618539483483'''

class FundIndustryCrawler:

    name = "行业配置数据"

    url = 'http://api.fund.eastmoney.com/f10/HYPZ'

    def __init__(self):
        self.params = self.format_params(params_str)

    def format_header(self, header_str=header_str):
        header = dict()
        for line in header_str.split('\n'):
            header[line.split(':')[0]] = ":".join(line.split(':')[1:])
        return header
    
    def format_params(self, params_str=params_str):
        params = dict()
        for line in params_str.split('\n'):
            params[line.split('=')[0]] = line.split('=')[1]
        return params


    def format_json(self, response, fund_code):
        # curr_info = response.split('(')
        curr_info = "(".join(response.split('(')[1:])[:-1]
        datas = json.loads(curr_info)['Data']
        final_datas = list()
        for QuarterInfos in datas["QuarterInfos"]:
            JZRQ = QuarterInfos['JZRQ'].replace('-', '')
            for HYPZInfo in QuarterInfos["HYPZInfo"]:
                HYPZInfo.update({"fund_code": fund_code, "_id": fund_code + JZRQ + HYPZInfo['HYDM']})
                final_datas.append(HYPZInfo)
        return final_datas
    
    def getFuncodeYears(self, fund_code):
        headers = self.format_header()
        self.params['fundCode'] = fund_code
        response = requests.get(self.url, params=self.params, headers=headers).text
        curr_info = "(".join(response.split('(')[1:])[:-1]
        return json.loads(curr_info)['Data']["ListYears"]


    def crawlFundIndustryList(self, fund_code="000001"):
        # if (dataControl.FundIndustryExsits(fund_code)):
        #     return
        years = self.getFuncodeYears(fund_code)
        headers = self.format_header()
        self.params['fundCode'] = fund_code
        for year in years:
            self.params['year'] = year
            response = requests.get(self.url, params=self.params, headers=headers)
            datas = self.format_json(response.text, fund_code)
            dataControl.insertFundIndustryInfos(datas)

if __name__ == "__main__":
    FundIndustryCrawler().crawlFundIndustryList("000041")