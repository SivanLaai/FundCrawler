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
    
    

global dataControl
dataControl = DataControl()