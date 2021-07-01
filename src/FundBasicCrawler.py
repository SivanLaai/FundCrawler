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
Referer:http://fundf10.eastmoney.com/jjjl_000041.html
Accept-Encoding:gzip, deflate
Accept-Language:zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7
If-Modified-Since:Sun, 25 Apr 2021 02:30:00 GMT'''


class FundBasicCrawler:

    name = "基金基本信息"

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
        fund_all_name = '' #基金全称
        fund_name = '' #基金简称
        fund_code = '' #基金代码
        fund_type = '' #基金类型
        issue_date = '' #发行日期
        found_date = ''#成立日期
        fund_scale = ''#基金规模
        asset = ''#资产规模
        share = ''#份额规模
        fund_company = '' #基金管理人，基金公司
        fund_trustee = ''# 基金托管人
        fund_current_manager = '' #基金经理
        dividend = ''#成立来分红
        management_fee_rate = ''#管理费率
        hosting_fees = ''#托管费率
        sales_service_rate = '' #销售服务费率
        max_subscription_rate = ''# 最高认购费率
        max_applyment_rate = '' #最高申购费率
        max_redemption_rate = ''#最高赎回费率
        performance_comparison_benchmark = ''#业绩比较基准
        target_track = ''#跟踪标的
        
        if len(curr_tree.xpath("//tr[1]/td[1]")) > 0: # /html/body/div[2]/div[8]/div[3]/div[2]/div[3]/div/div[1]/table/tbody/tr[1]/td[1]
            fund_all_name = curr_tree.xpath("//tr[1]/td[1]")[0].text
        if len(curr_tree.xpath("//tr[1]/td[2]")) > 0:
            fund_name = curr_tree.xpath("//tr[1]/td[2]")[0].text.replace('-', '')
        if len(curr_tree.xpath("//tr[2]/td[1]")) > 0:
            fund_code = curr_tree.xpath("//tr[2]/td[1]")[0].text.split('（')[0]
        if len(curr_tree.xpath("//tr[2]/td[2]")) > 0:
            fund_type = curr_tree.xpath("//tr[2]/td[2]")[0].text
        if len(curr_tree.xpath("//tr[3]/td[1]")) > 0:
            issue_date = curr_tree.xpath("//tr[3]/td[1]")[0].text.split('（')[0].replace('年', '').replace('月', '').replace('日', '')
        if len(curr_tree.xpath("//tr[3]/td[2]")) > 0:
            found_date, fund_scale = curr_tree.xpath("//tr[3]/td[2]")[0].text.split(' / ')
            found_date = found_date.replace('年', '').replace('月', '').replace('日', '')
        if len(curr_tree.xpath("//tr[4]/td[1]")) > 0:
            asset = curr_tree.xpath("//tr[4]/td[1]")[0].text
        if len(curr_tree.xpath("//tr[4]/td[2]/a")) > 0:
            share = curr_tree.xpath("//tr[4]/td[2]/a")[0].text
        if len(curr_tree.xpath("//tr[5]/td[1]/a")) > 0:
            fund_company = curr_tree.xpath("//tr[5]/td[1]/a")[0].get('href').split('/')[-1].split('.')[0]
        if len(curr_tree.xpath("//tr[5]/td[2]/a")) > 0:
            fund_trustee = curr_tree.xpath("//tr[5]/td[2]/a")[0].get('href').split('/')[-1].split('.')[0]

        if len(curr_tree.xpath("//tr[6]/td[1]/a")) > 0:
            fund_current_manager = curr_tree.xpath("//tr[6]/td[1]/a")[0].get('href').split('/')[-1].split('.')[0]
        if len(curr_tree.xpath("//tr[6]/td[2]/a")) > 0:
            dividend = curr_tree.xpath("//tr[6]/td[2]/a")[0].text
        if len(curr_tree.xpath("//tr[7]/td[1]")) > 0:
            management_fee_rate = curr_tree.xpath("//tr[7]/td[1]")[0].text
        if len(curr_tree.xpath("//tr[7]/td[2]")) > 0:
            hosting_fees = curr_tree.xpath("//tr[7]/td[2]")[0].text
        if len(curr_tree.xpath("//tr[8]/td[1]")) > 0:
            sales_service_rate = curr_tree.xpath("//tr[8]/td[1]")[0].text
        if len(curr_tree.xpath("//tr[8]/td[2]")) > 0:
            max_subscription_rate = curr_tree.xpath("//tr[8]/td[2]")[0].text
        if len(curr_tree.xpath("//td[1]/span[1]")) > 0:
            max_applyment_rate = curr_tree.xpath("//td[1]/span[1]")[0].text
            if len(curr_tree.xpath("//table/td[2]")) > 0:
                max_redemption_rate = curr_tree.xpath("//table/td[2]")[0].text
            if len(curr_tree.xpath("//tr[9]/td[1]")) > 0:
                performance_comparison_benchmark = curr_tree.xpath("//tr[9]/td[1]")[0].text
            if len(curr_tree.xpath("//tr[9]/td[2]")) > 0:
                target_track = curr_tree.xpath("//tr[9]/td[2]")[0].text
        else:
            if len(curr_tree.xpath("//tr[9]/td[1]")) > 0:
                max_applyment_rate = curr_tree.xpath("//tr[9]/td[1]")[0].text
            if len(curr_tree.xpath("//tr[9]/td[1]")) > 0:
                max_redemption_rate = curr_tree.xpath("//tr[9]/td[1]")[0].text
            if len(curr_tree.xpath("//tr[10]/td[1]")) > 0:
                performance_comparison_benchmark = curr_tree.xpath("//tr[10]/td[1]")[0].text
            if len(curr_tree.xpath("//tr[10]/td[2]")) > 0:
                target_track = curr_tree.xpath("//tr[10]/td[2]")[0].text

        curr_basic_dict = dict()
        curr_basic_dict['_id'] = str(fund_code) + str(issue_date)
        curr_basic_dict['fund_all_name'] = fund_all_name
        curr_basic_dict['fund_name'] = fund_name
        curr_basic_dict['fund_code'] = fund_code
        curr_basic_dict['fund_type'] = fund_type
        curr_basic_dict['issue_date'] = issue_date
        curr_basic_dict['found_date'] = found_date
        curr_basic_dict['fund_scale'] = fund_scale
        curr_basic_dict['asset'] = asset
        curr_basic_dict['share'] = share
        curr_basic_dict['fund_company'] = fund_company
        curr_basic_dict['fund_trustee'] = fund_trustee

        curr_basic_dict['fund_current_manager'] = fund_current_manager
        curr_basic_dict['dividend'] = dividend
        curr_basic_dict['management_fee_rate'] = management_fee_rate
        curr_basic_dict['hosting_fees'] = hosting_fees
        curr_basic_dict['sales_service_rate'] = sales_service_rate
        curr_basic_dict['max_subscription_rate'] = max_subscription_rate
        curr_basic_dict['max_applyment_rate'] = max_applyment_rate
        curr_basic_dict['max_redemption_rate'] = max_redemption_rate
        curr_basic_dict['performance_comparison_benchmark'] = performance_comparison_benchmark
        curr_basic_dict['target_track'] = target_track

        return curr_basic_dict
    
    def parserFundDesc(self, curr_tree, curr_basic_dict):
        investment_objective = ''#投资目标
        investment_concept = ''#投资理念
        investment_scope = ''#投资范围
        investment_tatics= ''#投资策略
        dividend_policy = ''#分红政策
        risk_revenue_traits = ''#风险收益特征

        if len(curr_tree.xpath("//div/div/div/div/div[2]/div/p")) > 0:
            investment_objective = curr_tree.xpath("//div/div/div/div/div[2]/div/p")[0].text
        if len(curr_tree.xpath("//div/div/div/div/div[3]/div/p")) > 0:
            investment_concept = curr_tree.xpath("//div/div/div/div/div[3]/div/p")[0].text
        if len(curr_tree.xpath("//div/div/div/div/div[4]/div/p")) > 0:
            investment_scope = curr_tree.xpath("//div/div/div/div/div[4]/div/p")[0].text
        if len(curr_tree.xpath("//div/div/div/div/div[5]/div/p")) > 0:
            investment_tatics = curr_tree.xpath("//div/div/div/div/div[5]/div/p")[0].text
        if len(curr_tree.xpath("//div/div/div/div/div[6]/div/p")) > 0:
            dividend_policy = curr_tree.xpath("//div/div/div/div/div[6]/div/p")[0].text
        if len(curr_tree.xpath("///div/div/div/div/div[7]/div/p")) > 0:
            risk_revenue_traits = curr_tree.xpath("///div/div/div/div/div[7]/div/p")[0].text

        curr_basic_dict['investment_objective'] = investment_objective
        curr_basic_dict['investment_concept'] = investment_concept
        curr_basic_dict['investment_scope'] = investment_scope
        curr_basic_dict['investment_tatics'] = investment_tatics
        curr_basic_dict['dividend_policy'] = dividend_policy
        curr_basic_dict['risk_revenue_traits'] = risk_revenue_traits
        return curr_basic_dict

    def format_json(self, response, fund_code):
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(str(response)), parser=parser)
        if tree is None:
            return final_datas
        final_datas = list()
        x_path = '//div/div/div/table'
        for curr_node in tree.xpath(x_path):
            curr_html = etree.tostring(curr_node)
            # print(curr_html)
            curr_tree = etree.parse(StringIO(str(curr_html)), parser=parser)
            curr_manager_dict = self.parseSingleNode(curr_tree, fund_code)
            curr_manager_dict = self.parserFundDesc(tree, curr_manager_dict)
            if curr_manager_dict is not None:
                final_datas.append(curr_manager_dict)
            break
        return final_datas


    def crawlFundBasicInfoList(self, fund_code="000001"):
        # if (dataControl.FundIndustryExsits(fund_code)):
        #     return
        headers = self.format_header()

        url = f"{self.url}/jbgk_{fund_code}.html"
        # print(url)
        response = requests.get(url, headers=headers)
        datas = self.format_json(response.text, fund_code)
        # print(datas)
        dataControl.insertFundBasicInfos(datas)

if __name__ == "__main__":
    FundBasicCrawler().crawlFundBasicInfoList("000497")