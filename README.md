# 轻量级基金爬虫
基金指标爬虫，抓取市面上所有基金信息\基金净值\基金成分\基金公司\基金经理
scrapy的框架太过厚重了，选用requests\execjs\lxml\selenium搭建了一个轻量级爬虫，可扩展性强，易于使用。
## 基金基本信息爬虫 AllFundCrawler
从网站上抓取所有开放基金的基本信息。
![Image text](/img/jbxx.png)

## 基金分红爬虫 FundDividendCrawler
![Image text](/img/fhxx.png)

## 基金成份爬虫 FundDividendCrawler
这个爬虫抓取的数据还是比较重要，主要是了解每只基金的组成的股票组合是什么，对于投资参考有很好的作用。
![Image text](/img/jjcf.png)

## 基金净值爬虫 FundTradeCrawler
抓取基金的过往历史数据，用于分析。
![Image text](/img/jjjz.png)

# 使用方法
### 0 python安装requests,lxml,pymongo,execjs,selenium
### 1 安装mongodb，最好配置用户权限，以免被攻击
### 2 配置setting
```bash
[SERVER]
port = 8010
host = 0.0.0.0
MAX_TRY = 10

[LOG]
LEVEL = INFO //日志等级
LOG_PATH = ./FundCrawler/logs //日志目录

[MONGO]
URL = 127.0.0.1 //MONGO服务器ip
PORT = 20137 //MONGO服务器端口
USERNAME = username
PASSWORD = password
DATA_BASE_NAME = Fund
ALL_FUND_COLLECTION = AllFundInfo
FUND_TRADE_COLLECTION = FundTradeInfo
FUND_STOCK_SHARE_COLLECTION = FundStockShare
FUND_BOND_SHARE_COLLECTION = FundBondShare
FUND_COMPANY_COLLECTION = FundCompany
FUND_DIVIDEND_COLLECTION = FundDividend
FUND_INDUSTRY_COLLECTION = FundIndustry
FUND_MANAGER_COLLECTION = FundManager
FUND_REVIEW_COLLECTION = FundReview
FUND_BASIC_COLLECTION = FundBasicInfo
```
### 3 运行爬虫
```bash
python src/CrawlerFacade.py
```