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

# fundcode=002190&showtype=0&year=&callback=jQuery18307902326421193109_1620391053363&_=1620391053373
params_str = '''fundCode=002190
showtype=1
year=
callback=jQuery1830379581891375977_1618539483467
_=1618539483483'''

class FundFinanceCrawler:

    name = "基金财务报表"

    url = 'http://api.fund.eastmoney.com/f10/GetArrayCwzb'

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
        datas = json.loads(curr_info)['Data']["data"]
        curr_data = dict()
        
        if "FSRQ" in datas:
            curr_data["FSRQ"] = datas["FSRQ"][0]
            curr_data["_id"] = f"{fund_code}{curr_data['FSRQ'].replace('-', '')}"
        if "COMPROFIT" in datas:
            curr_data["COMPROFIT"] = datas["COMPROFIT"][0]
        if "NETPROFIT" in datas:
            curr_data["NETPROFIT"] = datas["NETPROFIT"][0]
        if "UNITPROFIT" in datas:
            curr_data["UNITPROFIT"] = datas["UNITPROFIT"][0]
        if "NGROWTH" in datas:
            curr_data["NGROWTH"] = datas["NGROWTH"][0]
        if "FNGROWTH" in datas:
            curr_data["FNGROWTH"] = datas["FNGROWTH"][0]
        if "DISPROFIT" in datas:
            curr_data["DISPROFIT"] = datas["DISPROFIT"][0]
        if "DIFUNTIPROFIT" in datas:
            curr_data["DIFUNTIPROFIT"] = datas["DIFUNTIPROFIT"][0]
        if "ENDNAV" in datas:
            curr_data["ENDNAV"] = datas["ENDNAV"][0]
        if "ENDUNITNAV" in datas:
            curr_data["ENDUNITNAV"] = datas["ENDUNITNAV"][0]
        if "FCNGROWTH" in datas:
            curr_data["FCNGROWTH"] = datas["FCNGROWTH"][0]
        return curr_data
    
    def getFuncodeYears(self, fund_code):
        headers = self.format_header()
        self.params['fundCode'] = fund_code
        response = requests.get(self.url, params=self.params, headers=headers).text
        curr_info = "(".join(response.split('(')[1:])[:-1]
        return json.loads(curr_info)['Data']["years"]


    def crawlFundFinanceList(self, fund_code="000001"):
        # if (dataControl.FundIndustryExsits(fund_code)):
        #     return
        years = self.getFuncodeYears(fund_code)
        headers = self.format_header()
        self.params['fundCode'] = fund_code
        datas = list()
        for year in years:
            self.params['year'] = year
            response = requests.get(self.url, params=self.params, headers=headers)
            datas.append(self.format_json(response.text, fund_code))
        dataControl.insertFundFinanceInfos(datas)

if __name__ == "__main__":
    FundFinanceCrawler().crawlFundFinanceList("000041")