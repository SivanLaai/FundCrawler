import time
from Config import *
from Logger import logger
from AllFundCrawler import *
from FundTradeCrawler import *
from FundStockShare import *
from FundDividendCrawler import *
from FundReviewCrawler import *
from FundIndustryCrawler import *
from FundManagerHistoryCrawler import *
from FundBasicCrawler import *
from FundFinanceCrawler import *
import random


class CrawlerFacade:
    allFundCrawler = AllFundCrawler()
    fundTradeCrawler = FundTradeCrawler()
    fundStockShare = FundStockShare()
    fundDividendCrawler = FundDividendCrawler()
    fundReviewCrawler = FundReviewCrawler()
    fundIndustryCrawler = FundIndustryCrawler()
    fundManagerHistoryCrawler = FundManagerHistoryCrawler()
    fundBasicCrawler = FundBasicCrawler()
    fundFinanceCrawler = FundFinanceCrawler()


    def updateAllFundList(self):
        self.allFundCrawler.crawlFundList()

    def updateFrame(self, callback, name, index=0):
        fund_codes = self.allFundCrawler.getAllFundsCode()
        i = index
        while i < len(fund_codes): 
            try: 
                callback(fund_code=fund_codes[i])
                print('\r', f'更新基金的{name}数据：{i + 1} / {len(fund_codes)}', end='', flush=True)
                i = i + 1
                logger.info(f'更新基金{fund_codes[i - 1]}的{name}数据完成！')
            except Exception as e:
                time.sleep(random.randint(5, 10))
                errs = f"errors = {e}, retry funcode = {fund_codes[i]}"
                if "_id_ dup key" in errs:
                    i = i + 1
                logger.error(f"errors = {e}, retry funcode = {fund_codes[i]}")
        print()

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
                logger.error(f"errors = {e}, retry funcode = {fund_codes[i]}")
        print()
    
    # 更新所有基金的历史持仓数据
    def updateFundStockShareHistory(self):
        self.updateFrame(self.fundStockShare.crawlFundStockShareList, "历史持仓", 4497)
    
    # 更新所有基金的分红数据
    def updateFundDividendHistory(self):
        fund_codes = self.allFundCrawler.getAllFundsCode()
        i = 0
        print(len(fund_codes))
        while i < len(fund_codes): 
            fund_code = fund_codes[i]
            try:
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

    # 更新所有基金的评级数据
    def updateFundsReviewHistory(self):
        fund_codes = self.allFundCrawler.getAllFundsCode()
        i = 0
        while i < len(fund_codes): 
            try: 
                self.fundReviewCrawler.crawlReviewHistoryList(fund_code=fund_codes[i])
                print('\r', f'更新基金的历史交易数据：{i + 1} / {len(fund_codes)}', end='', flush=True)
                i = i + 1
                logger.info(f'更新基金{fund_codes[i - 1]}的历史交易数据完成！')
            except Exception as e:
                time.sleep(random.randint(5, 10))
                errs = f"errors = {e}, retry funcode = {fund_codes[i]}"
                if "_id_ dup key" in errs:
                    i = i + 1
                logger.error(f"errors = {e}, retry funcode = {fund_codes[i]}")
        print()
    
    def updateFundIndustryHistory(self):
        self.updateFrame(self.fundIndustryCrawler.crawlFundIndustryList, self.fundIndustryCrawler.name)

    def updateFundManagerHistory(self):
        self.updateFrame(self.fundManagerHistoryCrawler.crawlFundManagerInfoList, self.fundManagerHistoryCrawler.name)

    def updateFundBasic(self): 
        self.updateFrame(self.fundBasicCrawler.crawlFundBasicInfoList, self.fundBasicCrawler.name)

    def updateFundFinance(self): 
        self.updateFrame(self.fundFinanceCrawler.crawlFundFinanceList, self.fundFinanceCrawler.name)
    


if __name__ == '__main__':
    crawler = CrawlerFacade()
    #crawler.updateAllFundList()
    crawler.updateFundsTradeHistory()
    #crawler.updateFundStockShareHistory()
    #crawler.updateFundIndustryHistory()
    #crawler.updateFundDividendHistory()
    #crawler.updateFundsReviewHistory()
    #crawler.updateFundManagerHistory()
    #crawler.updateFundBasic()
    #crawler.updateFundFinance()
    # driver.close()
    # driver.quit()
