# shttps://www.guru99.com/chrome-options-desiredcapabilities.html



import selenium
import logging
#import pandas
import platform
import os



from selenium.webdriver.chrome.options import Options
######## for cbase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from log import customed_logger


class cbase():
    def __init__(self,path=None,headless=False):
        logging.info('init crawler')
        chrome_options = Options()
        if headless==True:
            chrome_options.add_argument('--headless')
            
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1280x1696')
        chrome_options.add_argument('--user-data-dir=/tmp/user-data')
        chrome_options.add_argument('--hide-scrollbars')
        chrome_options.add_argument('--enable-logging')
        chrome_options.add_argument('--log-level=0')
        chrome_options.add_argument('--v=99')
        chrome_options.add_argument('--single-process')
        chrome_options.add_argument('--data-path=/tmp/data-path')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--homedir=/tmp')
        chrome_options.add_argument('--disk-cache-dir=/tmp/cache-dir')
        chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')

        #chrome_options.binary_location = "/opt/python/bin/headless-chromium"
        
        
        if path ==None:
            _path = os.path.join(os.getcwd(),'local_crawler','src')
            
        if platform.platform().startswith('mac'):
            print("macOS call")
            target_string="chromedriver_mac"
        elif platform.platform().startswith('Linux') or platform.platform().startswith('linux') :
            print("linux")
            target_string="chromedriver_linux"
        
        target_string=target_string+"_103"
        
        _path = os.path.join(_path,target_string)
        self.driver = webdriver.Chrome(_path, options=chrome_options)
    
    def waiting(self,waitng_time):
        try:
            print("waiting")
            WebDriverWait(self.driver,10).until
                    
        
        finally:
            self.driver.quit()
        
        
    
if __name__=="__main__":
    '''
    크롤러의 기본 설정은 단위함수들의 pytest 용도로 사용 예정
    
    
    '''
    print("-------------------------")
    print("-------------------------")
    
        
    #### logging
    default=customed_logger('CRAWLER','./local_crawler/log/')
    default.logger.info('init start')
    c=cbase()
    c.driver.get("https://www.google.com")
    
    #### pytest
    ### Target_1. 공공 데이터 크롤링
    ### 데이터를 
    
    
    

    
    
    















