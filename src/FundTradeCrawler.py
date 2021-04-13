from Config import *
import requests
import lxml
import json
from DataControl import dataControl


header_str = '''Host:api.fund.eastmoney.com
Connection:keep-alive
User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.68
Accept:*/*
Referer:http://fundf10.eastmoney.com/
Accept-Encoding:gzip, deflate
Accept-Language:zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7
Content-Type:text/plain'''


params_str = '''callback=jQuery18306616460627646099_1617715660227
fundCode=000477
pageIndex=1
pageSize=100
startDate=
endDate=
_=1617715660245'''

class FundTradeCrawler:

    def __init__(self):
        self.params = self.format_params(params_str)

    def format_header(self, header_str=header_str):
        header = dict()
        for line in header_str.split('\n'):
            header[line.split(':')[0]] = ":".join(line.split(':')[1:])
        return header
    
    def format_params(self, params_str):
        params = dict()
        for line in params_str.split('\n'):
            params[line.split('=')[0]] = line.split('=')[1]
        return params

    def format_json(self, response, fund_code):
        # curr_info = response.split('(')
        curr_info = response.split('(')[1][:-1]
        datas = json.loads(curr_info)['Data']['LSJZList']
        final_datas = list()
        for data in datas:
            data.update({"fund_code": fund_code, "_id": fund_code + data["FSRQ"].replace('-', '')})
            final_datas.append(data)
        return final_datas

    def crawlHistoryList(self, fund_code="000001", page_index=1):
        headers = self.format_header()
        url = 'http://api.fund.eastmoney.com/f10/lsjz'
        self.params['fundCode'] = fund_code
        self.params['pageIndex'] = page_index
        response = requests.get(url, params=self.params, headers=headers)
        datas = self.format_json(response.text, fund_code)
        exists = dataControl.insertFundTradeInfos(datas)
        while len(datas) > 0 and exists:
            page_index = int(page_index) + 1
            self.params['pageIndex'] = page_index
            response = requests.get(url, params=self.params, headers=headers)
            datas = self.format_json(response.text, fund_code)
            exists = dataControl.insertFundTradeInfos(datas)

    def crawlAllHistoryList(self):
        headers = self.format_header()
        url = 'http://api.fund.eastmoney.com/f10/lsjz'
        
        # fund_infos = driver.find_element_by_xpath('/html/body/div[7]/div[3]/table[2]/tbody').text
        # pages = driver.find_elements(By.XPATH, '/html/body/div[7]/div[4]/div[2]/label')
        # page_num = len(pages)
        response = requests.get(url, params=self.params, headers=headers)
        datas = self.format_json(response.text, fund_code=self.params['fundCode'])
        dataControl.insertFundTradeInfos(datas)

      