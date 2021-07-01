from Config import *
import requests
import lxml
import json
import execjs
from DataControl import dataControl

header_str = '''Host:fund.eastmoney.com
Proxy-Connection:keep-alive
Accept:text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01
User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 Edg/90.0.818.49
X-Requested-With:XMLHttpRequest
Referer:http://fund.eastmoney.com/company/
Accept-Encoding:gzip, deflate
Accept-Language:zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7'''


data_keys ='datas:[],allRecords:7281,pageIndex:200,pageNum:50,allPages:146,allNum:7281,gpNum:1418,hhNum:3827,zqNum:1915,zsNum:1066,bbNum:0,qdiiNum:121,etfNum:0,lofNum:333,fofNum:155'

class AllFundCompany:

    def format_header(self, header_str=header_str):
        header = dict()
        for line in header_str.split('\n'):
            header[line.split(':')[0]] = ":".join(line.split(':')[1:])
        return header

    def get_data_keys(self, datas = data_keys):
        keys = set()
        for curr in datas.split(','):
            keys.add(curr.split(":")[0])
        return keys
    
    def getJSVariable(self, JS_code, variable_name='apidata'):
        cxt = execjs.compile(JS_code)
        return cxt.eval(variable_name)

    def format_json(self, response):
        json_datas = self.getJSVariable(response, "json")["datas"]
        # print(json_datas)
        # ['80000080','山西证券股份有限公司','1988-07-28','16','王怡里','SXZQ','','85.97','★★★','山西证券','','2021/3/31 0:00:00']
        datas = [{"_id": data[0], "fund_company_name": data[1], "company_found_date": data[2], "fund_manager_crew_num": data[3],
        "fund_company_boss_name": data[4], "fund_pinyin": data[5], "others1": data[6], "fund_manage_scale": data[7],
        "fund_company_rank": data[8], "fund_short_name": data[9], "others2": data[10], "update_time": data[11]} for data in json_datas]
        return datas
    
    def getAllFundsCode(self):
        fund_codes = [data['_id'] for data in dataControl.queryAllFundInfos()]
        # print(fund_codes)
        return fund_codes

    def crawlCompanyList(self):
        headers = self.format_header()
        print(headers)
        url = 'http://fund.eastmoney.com/Data/FundRankScale.aspx?_=1620388586790'
        
        response = requests.get(url, headers=headers)
        datas = self.format_json(response.text)
        # print(datas)
        dataControl.insertAllCompanyInfos(datas)

AllFundCompany().crawlCompanyList()

        