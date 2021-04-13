from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from itemadapter import is_item, ItemAdapter
import random
import json
import requests
import base64
import time
from scrapy.http import HtmlResponse
from selenium.webdriver.support.wait import WebDriverWait

from selenium import webdriver

class ParserBoss:
    def __init__(self):
        pass

    def parserAuthoritation(self):
        # ocr = PaddleOCR(use_gpu=False)
        # result = ocr.ocr("0e9ccdb6f22746076cd81c10bface6e6.jpg")
        # resume_info = ""
        # for line in result:
        #     resume_info += line[-1][0] + "\n"
        # print(resume_info)

        # 判断是否为登录界面
        url = "https://signup.zhipin.com/?intent=1&ka=header-boss"
        if "ka=header-boss" in url:
            # opt = webdriver.ChromeOptions()
            # opt.add_argument("--headless")
            # opt.add_argument("--disable-gpu")
            self.driver = webdriver.Edge("C:\Program Files (x86)\Microsoft\Edge\Application\msedgedriver.exe")
            self.driver.implicitly_wait(20)
            self.driver.get(url)
            print(url)

            self.login()

            response = self.get_image()

            coordinate_list = self.base64_api(response, 27).split("|")

            self.check(coordinate_list)

            # WebDriverWait(self.driver, 5, 0.2).until(lambda x: x.find_elements_by_xpath('//div[@class="geetest_result_tip"]'))
            # # 判断是否验证成功
            # while True:
            #     text = self.driver.find_elements_by_xpath('//div[@class="geetest_result_tip"]/text()')
            #     if len(text) == 0:
            #         break
            #     else:
            #         response = self.get_image()
            #         coordinate_list = self.base64_api(response, 27).split("|")
            #         self.check(coordinate_list)

            # # 点击登录
            # self.driver.find_element_by_xpath('//*[@id="wrap"]/div[2]/div[1]/div[2]/div[1]/form/div[6]/button').click()
            # # 搜索python职位
            # self.driver.find_element_by_xpath('//*[@id="container"]/div[2]/div/div[1]/button').click()
            # WebDriverWait(self.driver, 10, 0.2).until(lambda x: x.find_element_by_xpath('//*[@id="filter-box"]/div/div[1]/div/form/div[1]/p/input')).send_keys("python")
            # self.driver.find_element_by_xpath('//*[@id="filter-box"]/div/div[1]/div/form/button').click()
            # self.driver.execute_script("scrollTo(1000,100000)")

            # res = HtmlResponse(url=self.driver.current_url, body=self.driver.page_source, encoding="utf8", request=request)
            time.sleep(1)
            print("finished")
            # self.driver.quit()

    def base64_api(self, img,  typeid):
        """验证图片交给打码平台，返回验证坐标"""
        base64_data = base64.b64encode(img)
        b64 = base64_data.decode()
        data = {"username": "打码平台账号", "password": "打码平台密码", "image": b64, "typeid": typeid}
        result = json.loads(requests.post("http://api.ttshitu.com/imageXYPlus", json=data).text)
        if result['success']:
            return result["data"]["result"]
        else:
            return result["message"]
        return ""

    def login(self):
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="wrap"]/div[2]/div[4]/div[2]/div[1]/form/div[7]/a[3]').click()
        """输入账号密码，点击验证"""
        self.driver.find_element_by_xpath('//*[@id="wrap"]/div[2]/div[1]/div[2]/div[1]/form/div[3]/span[2]/input')\
            .send_keys("18612015279")
        self.driver.find_element_by_xpath('//*[@id="wrap"]/div[2]/div[1]/div[2]/div[1]/form/div[4]/span/input')\
            .send_keys("dvtc2007")
        self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[2]/div[1]/form/div[5]/div[1]/div').click()
        time.sleep(2)

    def get_image(self):
        """获取验证码图片"""
        image_url = self.driver.find_element_by_xpath('/html/body/div[5]/div[2]/div[1]/div/div/div[2]/div[1]/div/div[2]/img').get_attribute("src")
        headers = {"referer": "https://login.zhipin.com/"}
        response = requests.get(image_url).content
        return response

    def check(self, coordinate_list):
        """点选验证码"""
        action = webdriver.ActionChains(self.driver)
        image = self.driver.find_element_by_xpath('/html/body/div[5]/div[2]/div[1]/div/div/div[2]/div[1]/div/div[2]/img')
        for coordinate in coordinate_list:
            x, y = coordinate.split(",")
            action.move_to_element_with_offset(image, int(x), int(y))
            action.click()
        action.perform()
        self.driver.find_element_by_xpath('/html/body/div[5]/div[2]/div[1]/div/div/div[3]/a/div').click()

if __name__ == "__main__":
    # pb = ParserBoss()
    # pb.parserAuthoritation()
    import re
    companyPattern = "[\u4e00-\u9fa5（）()]+公司"
    text = '''达能乳业（北京）有限公司'''
    for company in re.compile(companyPattern).findall(text):
        print('company', company)


    try:
        pass
    except Exception as e:
        print(e)