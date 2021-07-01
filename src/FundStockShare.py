from Config import *
import requests
import json
from DataControl import dataControl
import execjs
from lxml import etree
from io import StringIO
from urllib.parse import unquote
from Logger import logger
import time

header_str = '''Host:fundf10.eastmoney.com
Proxy-Connection:keep-alive
User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.68
Accept:*/*
Referer:http://fundf10.eastmoney.com/ccmx_000001.html
Accept-Encoding:gzip, deflate
Accept-Language:zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7'''


params_str = '''type=jjcc
code=000001
topline=0
year=0
month=0
rt=0.9368076344308409'''

class FundStockShare:

    url = 'http://fundf10.eastmoney.com/FundArchivesDatas.aspx'

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
    
    def getJSVariable(self, JS_code, variable_name='apidata'):
        cxt = execjs.compile(JS_code)
        return cxt.eval(variable_name)

    
    def getFundStockYears(self, fund_code='000001'):
        params = self.format_params()
        headers = self.format_header()
        response = requests.get(self.url, params=params, headers=headers)
        curr_dict = self.getJSVariable(unquote(response.text))
        return curr_dict['arryear']

    def getFundStockHtmlContent(self, JS_code):
        curr_dict = self.getJSVariable(JS_code)
        return curr_dict['content']
    

    def parseSingleNode(self, curr_tree, fund_code, year, month):
        stock_code = ''
        stock_name = ''
        fund_share_portion = ''
        fund_share_numbers = ''
        fund_share_value = ''
        if len(curr_tree.xpath("//td[2]/a")) > 0:
            stock_code = curr_tree.xpath("//td[2]/a")[0].text
        if len(curr_tree.xpath("//td[2]/span")) > 0:
            stock_code = curr_tree.xpath("//td[2]/span")[0].text
        if len(curr_tree.xpath("//td[3]/a")) > 0:
            stock_name = curr_tree.xpath("//td[3]/a")[0].text
        if len(curr_tree.xpath("//td[3]/span")) > 0:
            stock_name = curr_tree.xpath("//td[3]/span")[0].text
        if len(curr_tree.xpath("//td[5]")) > 0:
            fund_share_portion = curr_tree.xpath("//td[5]")[0].text
        if len(curr_tree.xpath("//td[6]")) > 0:
            fund_share_numbers = curr_tree.xpath("//td[6]")[0].text
        if len(curr_tree.xpath("//td[7]")) > 0:
            fund_share_value = curr_tree.xpath("//td[7]")[0].text
        curr_fund_dict = dict()
        curr_fund_dict['_id'] = fund_code + str(year) + str(month) + stock_code
        curr_fund_dict['fund_code'] = fund_code
        curr_fund_dict['year'] = year
        curr_fund_dict['month'] = month
        curr_fund_dict['stock_code'] = stock_code
        curr_fund_dict['stock_name'] = stock_name
        curr_fund_dict['fund_share_portion'] = fund_share_portion
        curr_fund_dict['fund_share_numbers'] = fund_share_numbers
        curr_fund_dict['fund_share_value'] = fund_share_value
        return curr_fund_dict
    


    def parseHtml2Json(self, response_text, fund_code, year, month):
        final_datas = list()
        html_content = ""
        try:
            html_content = self.getFundStockHtmlContent(response_text)
            if len(html_content) <= 0:
                return final_datas
            # print("html_content; ", html_content)
            parser = etree.HTMLParser(encoding="utf-8")
            tree = etree.parse(StringIO(html_content), parser=parser)
            if tree is None:
                return final_datas
            for curr_node in tree.xpath('//div/div/table/tbody/tr'):
                curr_html = etree.tostring(curr_node)
                curr_tree = etree.parse(StringIO(str(curr_html)), parser=parser)
                # 格式化当前基金持仓信息
                curr_fund_dict = self.parseSingleNode(curr_tree, fund_code, year, month)
                final_datas.append(curr_fund_dict)
        except Exception as e:
                logger.error("html_content = %s, error = %s" %(html_content, e))
        return final_datas

    def crawlFundStockShareList(self, fund_code="000001"):
        if (dataControl.FundStockShareExsits(fund_code)):
            return
        headers = self.format_header()
        self.params['code'] = fund_code
        
        for year in self.getFundStockYears():
            for season in [1, 2, 3, 4]:
                self.params['year'] = year
                self.params['month'] = season * 3
                i = 1
                while i <= int(config["SERVER"]["MAX_TRY"]):
                    try:
                        response = requests.get(self.url, params=self.params, headers=headers)
                        datas = self.parseHtml2Json(response.text, fund_code, year, season * 3)
                        break
                    except Exception as e:
                        i = i + 1
                        logger.error(f"request url = {self.url} failed, retry.")
                        time.sleep(5)
                dataControl.insertFundStockShareInfos(datas)