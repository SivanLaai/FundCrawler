import json
from datetime import datetime
import time
from Config import *
from Logger import logger
import os
from AllFundCrawler import *
from FundTradeCrawler import *
from FundStockShare import *
from FundDividendCrawler import *
import random


class CrawlerFacade:
    allFundCrawler = AllFundCrawler()
    fundTradeCrawler = FundTradeCrawler()
    fundStockShare = FundStockShare()
    fundDividendCrawler = FundDividendCrawler()

    def updateAllFundList(self):
        self.allFundCrawler.crawlFundList()

    # 更新所有基金的历史交易数据
    def updateFundsTradeHistory(self):
        fund_codes = self.allFundCrawler.getAllFundsCode()
        i = 0
        while i < len(fund_codes): 
            try: 
                self.fundTradeCrawler.crawlHistoryList(fund_code=fund_codes[i])
                print('\r', f'更新基金的历史交易数据：{i + 1} / {len(fund_codes)}', end='', flush=True)
                i = i + 1
                logger.info(f'更新基金{fund_codes[i - 1]}的历史交易数据完成！')
            except Exception as e:
                time.sleep(random.randint(5, 10))
                errs = f"errors = {e}, retry funcode = {fund_codes[i]}"
                if "_id_ dup key" in errs:
                    i = i + 1
                logger.error(f"errors = {e}, retry funcode = {fund_code}")
        print()
    
    # 更新所有基金的历史持仓数据
    def updateFundStockShareHistory(self):
        fund_codes = self.allFundCrawler.getAllFundsCode()
        i = 0
        while i < len(fund_codes): 
            try: 
                print('\r', f'更新所有基金的历史持仓数据：{i + 1} / {len(fund_codes)}', end='', flush=True)
                self.fundStockShare.crawlFundStockShareList(fund_code=fund_codes[i])
                i = i + 1
            except Exception as e:
                time.sleep(random.randint(5, 10))
                errs = f"errors = {e}, retry funcode = {fund_codes[i]}"
                if "_id_ dup key" in errs:
                    i = i + 1
                logger.error(f"errors = {e}, retry funcode = {fund_code}")
        print()
    
    # 更新所有基金的分红数据
    def updateFundDividendHistory(self):
        fund_codes = self.allFundCrawler.getAllFundsCode()
        i = 0
        print(len(fund_codes))
        while i < len(fund_codes): 
            try:
                fund_code = fund_codes[i]
                self.fundDividendCrawler.crawlDividendHistoryList(fund_code)
                print('\r', f'更新所有基金{fund_code}的分红数据,当前进度{i + 1} / {len(fund_codes)}', end='', flush=True)
                # print(f'更新所有基金的分红数据{i + 1}')
                if i % 110:
                    time.sleep(random.randint(5, 10))
                else:
                    time.sleep(random.random())
                i = i + 1
            except Exception as e:
                time.sleep(random.randint(5, 10))
                logger.error(f"errors = {e}, retry funcode = {fund_code}")
        print()
    

    # 更新所有数据
    # def updateFundStockShareHistory(self):
    #     fund_codes = self.allFundCrawler.getAllFundsCode()
    #     for i in range(len(fund_codes)): 
    #         self.fundStockShare.crawlFundStockShareList(fund_code=fund_codes[i])
    #         print('\r', f'更新所有基金的历史持仓数据：{i + 1} / {len(fund_codes)}', end='', flush=True)
    #         if i % 110:
    #             time.sleep(random.randint(5, 10))
    #         else:
    #             time.sleep(0.3)
    #     print()


if __name__ == '__main__':
    crawler = CrawlerFacade()
    # crawler.updateAllFundList()
    crawler.updateFundsTradeHistory()
    # crawler.updateFundStockShareHistory()
    # crawler.updateFundDividendHistory()
    driver.close()
    driver.quit()