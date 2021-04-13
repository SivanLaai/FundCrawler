from Config import *
from selenium.webdriver.common.by import By

class AllFundCrawler_Selenium:
    def parserCurrentPage(self, x_path = '/html/body/div[7]/div[3]/table[2]/tbody/tr'):
        fund_infos = driver.find_elements(By.XPATH, x_path)
        f = open('fund_all.csv', 'w')
        for i in range(len(fund_infos)):
            curr_x_path = x_path + '[%d]'%(i + 1)
            fund_info_list = driver.find_element(By.XPATH, curr_x_path)
            #print(fund_info_list.text.replace('\n', ',').replace(' ', ','))
            f.write(fund_info_list.text.replace('\n', ',').replace(' ', ',') + '\n')
            f.flush()
        f.close()

    def getFundList(self):
        url = 'http://fund.eastmoney.com/data/fundranking.html#tall;c0;r;sdm;pn50;dasc;qsd20200406;qed20210406;qdii;zq;gg;gzbd;gzfs;bbzt;sfbb'
        driver.get(url)
        driver.find_element_by_xpath('/html/body/div[7]/div[4]/div[3]/label/input').click()
        # fund_infos = driver.find_element_by_xpath('/html/body/div[7]/div[3]/table[2]/tbody').text
        # pages = driver.find_elements(By.XPATH, '/html/body/div[7]/div[4]/div[2]/label')
        # page_num = len(pages)

        driver.implicitly_wait(50)

        # # 解析当前页面的基金信息
        self.parserCurrentPage()

        # # 获取结束标识 end
        # flag = driver.find_element_by_xpath('/html/body/div[7]/div[4]/div[2]/label[%d]' % page_num).get_attribute("class")
        # while flag != "end":
        #     driver.implicitly_wait(20)
        #     pages = driver.find_elements(By.XPATH, '/html/body/div[7]/div[4]/div[2]/label')
        #     page_num = len(pages)
        #     ## 点击下一页
        #     driver.find_element_by_xpath('/html/body/div[7]/div[4]/div[2]/label[%d]' % page_num).click()
        #     # fund_infos = driver.find_element_by_xpath('/html/body/div[7]/div[3]/table[2]/tbody').text
        #     # print(fund_infos)
        #     self.parserCurrentPage()
        #     #print(fund_infos)