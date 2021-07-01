import pymongo
from Config import *
from urllib.parse import quote_plus

class DataControl:
    uri = "mongodb://%s:%s" % (quote_plus(config["MONGO"]["URL"]), quote_plus(config["MONGO"]["PORT"]))
    myclient = pymongo.MongoClient(uri)
    mydb = myclient[config["MONGO"]["DATA_BASE_NAME"]]  
    mydb.authenticate(config["MONGO"]["USERNAME"], config["MONGO"]["PASSWORD"])
    
    def insertAllFundInfos(self, allFundInfos = []):
        if len(allFundInfos) <= 0:
            return
        allFundCol = self.mydb[config["MONGO"]["ALL_FUND_COLLECTION"]]
        # print(allFundInfos)
        allFundCol.insert_many(allFundInfos) #, upsert=True
    
    def queryAllFundInfos(self):
        allFundCol = self.mydb[config["MONGO"]["ALL_FUND_COLLECTION"]]
        allFundList = allFundCol.find()
        return list(allFundList)
    
    def batchInsert(self, table_name, datas):
        if len(datas) <= 0:
            return True
        fundTradeCol = self.mydb[config["MONGO"][table_name]]
        no_exist_list = list()

        # 当前的表格中存在与插入的数据相同的数据，则直接返回False
        for data in datas:
            # print(fundTradeInfos)
            if fundTradeCol.find_one({"_id": data['_id']}) is not None:
                if len(no_exist_list) <= 0:
                    return False
                fundTradeCol.insert_many(no_exist_list)
                return False
            no_exist_list.append(data)
        fundTradeCol.insert_many(datas)
        # print(datas)
        return True


    '''
    批量的向数据表格中插入数据，如果表格中有这些数据那么就不在插入
    - Paramaters:
        fundTradeInfos ： 代插入的数据
    - Return:
        Flase: 当前所有的数据都不存在于表格中 
        True: 当前的数据在表格中有重复数据
    '''
    def insertFundTradeInfos(self, fundTradeInfos = []):
        if len(fundTradeInfos) <= 0:
            return True
        fundTradeCol = self.mydb[config["MONGO"]["FUND_TRADE_COLLECTION"]]
        no_exist_list = list()

        # 当前的表格中存在与插入的数据相同的数据，则直接返回False
        for data in fundTradeInfos:
            # print(fundTradeInfos)
            if fundTradeCol.find_one({"_id": data['_id']}) is not None:
                if len(no_exist_list) <= 0:
                    return False
                fundTradeCol.insert_many(no_exist_list)
                return False
            no_exist_list.append(data)
        fundTradeCol.insert_many(fundTradeInfos)
        return True
    
    '''
    批量的向数据表格中插入数据，如果表格中有这些数据那么就不在插入
    - Paramaters:
        fundTradeInfos ： 代插入的数据
    - Return:
        Flase: 当前所有的数据都不存在于表格中 
        True: 当前的数据在表格中有重复数据
    '''
    def insertFundStockShareInfos(self, fundStockShareInfos = []):
        if len(fundStockShareInfos) <= 0:
            return True
        fundStockShareCol = self.mydb[config["MONGO"]["FUND_STOCK_SHARE_COLLECTION"]]
        no_exist_list = list()

        # 当前的表格中存在与插入的数据相同的数据，则直接返回False
        for data in fundStockShareInfos:
            # print(fundTradeInfos)
            if fundStockShareCol.find_one({"_id": data['_id']}) is not None:
                if len(no_exist_list) <= 0:
                    return False
                fundStockShareCol.insert_many(no_exist_list)
                return False
            no_exist_list.append(data)
        fundStockShareCol.insert_many(fundStockShareInfos)
        return True

    def FundStockShareExsits(self, fund_code):
        fundStockShareCol = self.mydb[config["MONGO"]["FUND_STOCK_SHARE_COLLECTION"]]
        if fundStockShareCol.find_one({"fund_code": fund_code}) is not None:
            return True
        return False
    
    
    '''
    批量的向数据表格中插入数据，如果表格中有这些数据那么就不在插入
    - Paramaters:
        fundTradeInfos ： 代插入的数据
    - Return:
        Flase: 当前所有的数据都不存在于表格中 
        True: 当前的数据在表格中有重复数据
    '''
    def insertFundDividendInfos(self, fundDividendInfos = []):
        if len(fundDividendInfos) <= 0:
            return True
        fundDividendCol = self.mydb[config["MONGO"]["FUND_DIVIDEND_COLLECTION"]]
        no_exist_list = list()

        # 当前的表格中存在与插入的数据相同的数据，则直接返回False
        for data in fundDividendInfos:
            if fundDividendCol.find_one({"_id": data['_id']}) is not None:
                if len(no_exist_list) <= 0:
                    return False
                fundDividendCol.insert_many(no_exist_list)
                return False
            no_exist_list.append(data)
        fundDividendCol.insert_many(fundDividendInfos)
        return True
    
    '''
    批量的向数据表格中插入数据，如果表格中有这些数据那么就不在插入
    - Paramaters:
        fundReviewInfos ： 代插入的数据，同行评级
    - Return:
        Flase: 当前所有的数据都不存在于表格中 
        True: 当前的数据在表格中有重复数据
    '''
    def insertFundReviewInfos(self, fundReviewInfos = []):
        if len(fundReviewInfos) <= 0:
            return True
        fundViewCol = self.mydb[config["MONGO"]["FUND_REVIEW_COLLECTION"]]
        no_exist_list = list()

        # 当前的表格中存在与插入的数据相同的数据，则直接返回False
        for data in fundReviewInfos:
            # print(fundTradeInfos)
            if fundViewCol.find_one({"_id": data['_id']}) is not None:
                if len(no_exist_list) <= 0:
                    return False
                fundViewCol.insert_many(no_exist_list)
                return False
            no_exist_list.append(data)
        fundViewCol.insert_many(fundReviewInfos)
        return True
    
    '''
    批量的向数据表格中插入数据，如果表格中有这些数据那么就不在插入
    - Paramaters:
        fundIndustryInfos ： 代插入的数据，行业配置
    - Return:
        Flase: 当前所有的数据都不存在于表格中 
        True: 当前的数据在表格中有重复数据
    '''
    def insertFundIndustryInfos(self, fundIndustryInfos = []):
        if len(fundIndustryInfos) <= 0:
            return True
        Col = self.mydb[config["MONGO"]["FUND_INDUSTRY_COLLECTION"]]
        no_exist_list = list()

        # 当前的表格中存在与插入的数据相同的数据，则直接返回False
        for data in fundIndustryInfos:
            # print(fundTradeInfos)
            if Col.find_one({"_id": data['id']}) is not None:
                if len(no_exist_list) <= 0:
                    return False
                Col.insert_many(no_exist_list)
                return False
            no_exist_list.append(data)
        Col.insert_many(fundIndustryInfos)
        return True
    
    '''
    批量的向数据表格中插入数据，如果表格中有这些数据那么就不在插入
    - Paramaters:
        Infos ： 代插入的数据，基金的基金经理历史数据
    - Return:
        Flase: 当前所有的数据都不存在于表格中 
        True: 当前的数据在表格中有重复数据
    '''
    def insertFundManagerHistoryInfos(self, Infos = []):
        if len(Infos) <= 0:
            return True
        Col = self.mydb[config["MONGO"]["FUND_MANAGER_HISTORY_COLLECTION"]]
        no_exist_list = list()

        # 当前的表格中存在与插入的数据相同的数据，则直接返回False
        for data in Infos:
            # print(fundTradeInfos)
            if Col.find_one({"_id": data['_id']}) is not None:
                if len(no_exist_list) <= 0:
                    return False
                Col.insert_many(no_exist_list)
                return False
            no_exist_list.append(data)
        Col.insert_many(Infos)
        return True
    
    '''
    批量的向数据表格中插入数据，如果表格中有这些数据那么就不在插入
    - Paramaters:
        Infos ： 代插入的数据，基金的基金经理历史数据
    - Return:
        Flase: 当前所有的数据都不存在于表格中 
        True: 当前的数据在表格中有重复数据
    '''
    def insertFundBasicInfos(self, datas = []):
        return self.batchInsert("FUND_BASIC_COLLECTION", datas)
    
    '''
    批量的向数据表格中插入数据，如果表格中有这些数据那么就不在插入
    - Paramaters:
        datas ： 代插入的数据，ALL_FUND_COMPANY_COLLECTION数据
    - Return:
        Flase: 当前所有的数据都不存在于表格中 
        True: 当前的数据在表格中有重复数据
    '''
    def insertAllCompanyInfos(self, datas = []):
        return self.batchInsert("ALL_FUND_COMPANY_COLLECTION", datas)

    
    def insertFundFinanceInfos(self, datas = []):
        return self.batchInsert("FUND_FINANCE_COLLECTION", datas)
    

global dataControl
dataControl = DataControl()
