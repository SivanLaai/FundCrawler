from Config import *
import requests
import lxml
import json
from DataControl import dataControl

header_str = '''Host:fund.eastmoney.com
Proxy-Connection:keep-alive
User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.68
Accept:*/*
Referer:http://fund.eastmoney.com/data/fundranking.html
Accept-Encoding:gzip, deflate
Accept-Language:zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7
Content-Type:text/plain'''
params_str = '''op=ph
dt=kf
ft=all
rs=
gs=0
sc=dm
st=asc
sd=2020-04-06
ed=2021-04-06
qdii=
tabSubtype=,,,,,
pi=1= 页数
pn=100
dx=1
v=0.46754866961417463'''

data_keys ='datas:[],allRecords:7281,pageIndex:200,pageNum:50,allPages:146,allNum:7281,gpNum:1418,hhNum:3827,zqNum:1915,zsNum:1066,bbNum:0,qdiiNum:121,etfNum:0,lofNum:333,fofNum:155'

class AllFundCrawler:

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

    def get_data_keys(self, datas = data_keys):
        keys = set()
        for curr in datas.split(','):
            keys.add(curr.split(":")[0])
        return keys

    def format_json(self, response):
        curr_info = response.replace(' ', '').split('=')[-1][:-1]
        for key in self.get_data_keys():
            curr_info = curr_info.replace(key, '"%s"'%key)
        response = json.loads(curr_info)
        datas = list()
        # ['000021', '华夏优势增长混合', 'HXYSZZHH', '2021-04-06', '2.8910', '4.0610', '-0.14', '1.87', '-1.53', '-12.42', '15.96', '54.60', '69.16', '69.26', '-7.10', '492.0360', '2006-11-24', '1', '50.5729', '1.50%', '0.15%', '1', '0.15%', '1', '72.29']
        fund_info_keys = ["_id", "fund_name", "fund_pinyin", 'date', "net_asset_value", "accumulated_unit_value", 'day_growth_rate', 'week_growth_rate', "month_growth_rate", "season_growth_rate",	"half_year_growth_rate", "year_growth_rate", "two_year_growth_rate","three_year_growth_rate", "this_year_growth_rate", "accumulated_growth_rate", "fund_founded_date", "var1",  "custome_growth_rate", "var2", "fees", "var3", "var4", "var5", "var6"]
        for data in response['datas']:
            data_dict = {k : v for k, v in zip(fund_info_keys, data.split(','))}
            # print(data.split(','))
            datas.append(data_dict)
        return datas
    
    def getAllFundsCode(self):
        fund_codes = [data['_id'] for data in dataControl.queryAllFundInfos()]
        # print(fund_codes)
        return fund_codes

    def crawlFundList(self):
        headers = self.format_header()
        params = self.format_params()
        url = 'http://fund.eastmoney.com/data/rankhandler.aspx'
        
        response = requests.get(url, params=params, headers=headers)
        datas = self.format_json(response.text)
        dataControl.insertAllFundInfos(datas)
        f = open(config["DATA"]["ALL_FUND_PATH"], 'w')
        count = len(datas)
        while len(datas) > 0:
            try:
                params["pi"] = int(params["pi"]) + 1
                response = requests.get(url, params=params, headers=headers)
                datas = self.format_json(response.text)
                #print(datas)
                print('\r', f'已更新{count}个基金数据', end='', flush=True)
                count = count + len(datas)
                dataControl.insertAllFundInfos(datas)
            except Exception as e:
                params["pi"] = int(params["pi"]) - 1
                print(f"error: {e}, try again!")
# AllFundCrawler().crawlFundList()

        