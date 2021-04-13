#coding:utf-8
from Config import *
import requests
import lxml
import json
from DataControl import dataControl
from Logger import *
from lxml import etree
from io import StringIO, BytesIO


header_str = '''Host:fundf10.eastmoney.com
Proxy-Connection:keep-alive
Cache-Control:max-age=0
Upgrade-Insecure-Requests:1
User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.68
Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer:http://fund.eastmoney.com/
Accept-Encoding:gzip, deflate
Accept-Language:zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7
If-Modified-Since:Fri, 09 Apr 2021 07:50:00 GMT'''


class FundDividendCrawler:

    url = 'http://fundf10.eastmoney.com'

    def format_header(self, header_str=header_str):
        header = dict()
        for line in header_str.split('\n'):
            header[line.split(':')[0]] = ":".join(line.split(':')[1:])
        return header
    

    def parseSingleNode(self, curr_tree, fund_code):
        year = '' #分红年份
        registration_date = '' #权益登记日			
        ex_dividend_date = '' #除息日
        per_share_dividend = '' #每份分红
        dividend_date = ''#分红发放日
        if len(curr_tree.xpath("//tr/td[1]")) > 0:
            year = curr_tree.xpath("//tr/td[1]")[0].text[:-1]
        if len(curr_tree.xpath("//tr/td[2]")) > 0:
            registration_date = curr_tree.xpath("//tr/td[2]")[0].text.replace('-', '')
        if len(curr_tree.xpath("//tr/td[3]")) > 0:
            ex_dividend_date = curr_tree.xpath("//tr/td[3]")[0].text.replace('-', '')
        if len(curr_tree.xpath("//tr/td[4]")) > 0:
            per_share_dividend = curr_tree.xpath("//tr/td[4]")[0].text.replace('-', '')
        if len(curr_tree.xpath("//tr/td[5]")) > 0:
            dividend_date = curr_tree.xpath("//tr/td[5]")[0].text.replace('-', '')
        curr_dividend_dict = dict()
        curr_dividend_dict['_id'] = str(fund_code) + str(registration_date)
        curr_dividend_dict['fund_code'] = fund_code
        curr_dividend_dict['year'] = year
        curr_dividend_dict['registration_date'] = registration_date
        curr_dividend_dict['ex_dividend_date'] = ex_dividend_date
        curr_dividend_dict['per_share_dividend'] = per_share_dividend
        curr_dividend_dict['dividend_date'] = dividend_date
        return curr_dividend_dict
    


    def parseHtml2Json(self, html_content, fund_code):
        final_datas = list()
        try:
            if len(html_content) <= 0:
                return final_datas
            # print("html_content; ", html_content)
            parser = etree.HTMLParser()
            tree = etree.parse(StringIO(str(html_content)), parser=parser)
            if tree is None:
                return final_datas
            f = open("index.html", 'w')
            f.write(html_content)
            f.flush()
            f.close()
            for curr_node in tree.xpath('//div/div/table/tbody/tr'):
                curr_html = etree.tostring(curr_node)
                curr_tree = etree.parse(StringIO(str(curr_html)), parser=parser)
                # 格式化当前的基金分红信息
                curr_fund_dict = self.parseSingleNode(curr_tree, fund_code)
                
                if curr_fund_dict["year"] == "暂无拆分信息" or curr_fund_dict["per_share_dividend"] == "":
                    continue
                # print(curr_fund_dict)
                final_datas.append(curr_fund_dict)
        except Exception as e:
                logger.error("html_content = %s, error = %s" %(html_content[:100], e))
        return final_datas

    def crawlDividendHistoryList(self, fund_code="000001"):
        headers = self.format_header()
        url = self.url + f'/fhsp_{fund_code}.html'
        # print(url)
        response = requests.get(url, headers=headers)
        datas = self.parseHtml2Json(response.text, fund_code)
        dataControl.insertFundDividendInfos(datas)

# FundDividendCrawler().crawlDividendHistoryList()
# headers = {'Host': 'fundf10.eastmoney.com', 'Proxy-Connection': 'keep-alive', 'Cache-Control': 'max-age=0', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.68', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Referer': 'http://fund.eastmoney.com/', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7', 'If-Modified-Since': 'Fri, 09 Apr 2021 07:50:00 GMT', 'Content-Type': 'text/plain'}
# response = requests.get("http://fundf10.eastmoney.com/fhsp_000001.html", headers=headers)
# print(response.content)
