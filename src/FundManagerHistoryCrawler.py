from Config import *
import requests
import json
from DataControl import dataControl
import execjs
from lxml import etree
from io import StringIO, BytesIO
from Logger import logger
import time

header_str = '''Host:fundf10.eastmoney.com
Proxy-Connection:keep-alive
Cache-Control:max-age=0
Upgrade-Insecure-Requests:1
User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36 Edg/90.0.818.42
Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer:http://fund.eastmoney.com/
Accept-Encoding:gzip, deflate
Accept-Language:zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7
Content-Type:text/plain'''


class FundManagerHistoryCrawler:

    name = "基金经理历史信息"

    url = 'http://fundf10.eastmoney.com'

    def __init__(self):
        pass

    def format_header(self, header_str=header_str):
        header = dict()
        for line in header_str.split('\n'):
            header[line.split(':')[0]] = ":".join(line.split(':')[1:])
        return header

    
    def parserManagerInfo(self, curr_tree):
        manager_id = ''
        for manager_node in curr_tree.xpath("//td/a"):
            manager_id = manager_id + ',' + manager_node.get("href").split('/')[-1].split('.')[0]
        manager_id = manager_id[1:]
        # print(manager_id)
        return manager_id
    

    def parseSingleNode(self, curr_tree, fund_code):
        start_date = '' #起始期			
        end_date = '' #截止期
        manager_info = ''# 基金经理
        duration = '' #任职期间
        return_rate = ''#任职回报
        
        if len(curr_tree.xpath("//tr/td[1]")) > 0:
            if curr_tree.xpath("//tr/td[1]")[0].text is None:
                return None
            start_date = curr_tree.xpath("//tr/td[1]")[0].text.replace('-', '')
        if len(curr_tree.xpath("//tr/td[2]")) > 0:
            end_date = curr_tree.xpath("//tr/td[2]")[0].text.replace('-', '')
        if len(curr_tree.xpath("//tr/td[3]")) > 0:
            parser = etree.HTMLParser()
            curr_html = etree.tostring(curr_tree.xpath("//tr/td[3]")[0])
            curr_manager_tree = etree.parse(StringIO(str(curr_html)), parser=parser)
            manager_info = self.parserManagerInfo(curr_manager_tree) # curr_tree.xpath("//tr/td[3]")[0].text.replace('-', '')
        if len(curr_tree.xpath("//tr/td[4]")) > 0:
            duration = curr_tree.xpath("//tr/td[4]")[0].text
        if len(curr_tree.xpath("//tr/td[5]")) > 0:
            return_rate = curr_tree.xpath("//tr/td[5]")[0].text
        curr_manager_dict = dict()
        curr_manager_dict['_id'] = str(fund_code) + str(start_date)
        curr_manager_dict['fund_code'] = fund_code
        curr_manager_dict['start_date'] = start_date
        curr_manager_dict['end_date'] = end_date
        curr_manager_dict['manager_info'] = manager_info
        curr_manager_dict['duration'] = duration
        curr_manager_dict['return_rate'] = return_rate
        return curr_manager_dict

    def format_json(self, response, fund_code):
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(str(response)), parser=parser)
        final_datas = list()

        if tree is None:
            return final_datas
        # print(tree.xpath('//div/table/tbody'))
        for curr_node in tree.xpath('//div/div/div/div/div/div/div/table/tbody/tr'):
            curr_html = etree.tostring(curr_node)
            curr_tree = etree.parse(StringIO(str(curr_html)), parser=parser)
            curr_manager_dict = self.parseSingleNode(curr_tree, fund_code)
            if curr_manager_dict is not None:
                final_datas.append(curr_manager_dict)
        return final_datas


    def crawlFundManagerInfoList(self, fund_code="000001"):
        # if (dataControl.FundIndustryExsits(fund_code)):
        #     return
        headers = self.format_header()

        url = f"{self.url}/jjjl_{fund_code}.html"
        print(url)
        response = requests.get(url, headers=headers)
        datas = self.format_json(response.text, fund_code)
        print(dataControl.insertFundManagerHistoryInfos(datas))

if __name__ == "__main__":
    FundManagerInfoCrawler().crawlFundManagerInfoList("000041")
